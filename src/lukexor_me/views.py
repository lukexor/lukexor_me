from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import View
from honeypot.decorators import check_honeypot
from lukexor_me import forms, models
from lib.site_search import SiteSearch
import logging, datetime, hashlib, lib

handler400 = 'lukexor_me.views.BadRequestView'
handler403 = 'lukexor_me.views.PermissionDeniedView'
handler404 = 'lukexor_me.views.PageNotFoundView'
handler500 = 'lukexor_me.views.ServerErrorView'
logger = logging.getLogger(__name__)

def build_page_title(title):
    return '%s :: %s' % (title, settings.STRINGS['full_name'])

def get_article_tags():
    tags = cache.get('article_tags')

    if not tags:
        tags = models.Tag.objects.filter(article__isnull=False).distinct()
        cache.set('article_tags', tags, settings.CACHE_TIMES['labels'])

    return tags

def get_project_tags():
    tags = cache.get('project_tags')

    if not tags:
        tags = models.Tag.objects.filter(project__isnull=False).distinct()
        cache.set('project_tags', tags, settings.CACHE_TIMES['labels'])

    return tags

def get_article_categories():
    categories = cache.get('categories')

    if not categories:
        categories = models.Category.objects.filter(article__isnull=False).distinct()
        cache.set('categories', categories, settings.CACHE_TIMES['labels'])

    return categories

def get_prev_page(page):
    if int(page) > 0:
        return int(page) - 1
    else:
        return None

def get_next_page(page, limit, count):
    if count > ( (int(page) + 1) * limit ):
        return int(page) + 1
    else:
        return None

def get_page_offset(page, limit):
    return int(page) * limit

def create_results_string(count, offset, limit):
    count_string = ""
    page_starting_number = offset + 1
    page_ending_number = limit + offset

    if (page_starting_number >= count):
        count_string += "%d of %d" % (page_starting_number, count)
    elif (count > limit):
        count_string += "%d" % (page_starting_number)
        count_string += " - %d of %d" % (page_ending_number, count)
    else:
        count_string += "%d" % (count)

    count_string += " result"

    if (count != 1):
        count_string += "s"

    return count_string

def project_view(request, project, form):
    return render(request, "projects.html", {
        'comments_enabled': settings.COMMENTS_ENABLED,
        'form': form,
        'page_description': project.title + " :: " + project.summary(),
        'page_keywords': project.get_tags(),
        'page_title': build_page_title(project.title),
        'projects': [project],
        'show_comments': True,
        'tags': get_project_tags(),
        'website': '',
    })

def article_view(request, article, form):
    filter = { 'date_published__lte': timezone.now() }
    order_by = [ '-date_published' ]

    # Display unpublished articles to admin users
    if request.user.is_authenticated() and request.user.has_perm('lukexor_me.change_article'):
        filter = {}
        order_by = [ '-created', '-date_published' ]

    all_articles = models.Article.objects.filter(**filter).order_by(*order_by)

    return render(request, "articles.html", {
        'articles': [article],
        'archive': datify_archive(all_articles),
        'categories': get_article_categories(),
        'comments_enabled': settings.COMMENTS_ENABLED,
        'form': form,
        'page_description': article.title + " :: " + article.summary(),
        'page_keywords': article.get_tags(),
        'page_title': build_page_title(article.title),
        'show_comments': True,
        'tags': get_article_tags(),
        'website': '',
    })

def datify_archive(entries):
    archive = cache.get('datified_archive')

    if not archive:
        archive = []

        for entry in entries:
            year = None
            month = None

            if entry.date_published:
                year = entry.date_published.strftime('%Y')
                month = entry.date_published.strftime('%m')
                month_name = entry.date_published.strftime('%b')
            elif entry.created:
                year = entry.created.strftime('%Y')
                month = entry.created.strftime('%m')
                month_name = entry.created.strftime('%b')

            if year and month:
                entry_data = {
                    "title": entry.title,
                    "permalink": reverse_lazy('article_permalink', args=[year, month, entry.permalink_title]),
                }

                year_match = next((entry for entry in archive if entry['year'] == year), None)
                if year_match:
                    month_match = next((entry for entry in year_match['months'] if entry['name'] == month_name), None)
                    if month_match:
                        month_match['posts'].append(entry_data)
                    else:
                        month_data = {
                            "name": month_name,
                            "posts": [entry_data],
                        }
                        year_match['months'].append(month_data)
                else:
                    year_data = {
                        "year": year,
                        "months": [{
                            "name": month_name,
                            "posts": [entry_data]
                        }],
                    }
                    archive.append(year_data)

        cache.set('datified_archive', archive, settings.CACHE_TIMES['post'])

    return archive


class BadRequestView(View):

    def get(self, request):
        return render(request, "400.html", {'page_title': build_page_title('400 FLAGRANT SYSTEM ERROR'), 'page_keywords': '', 'website': ''})


class PermissionDeniedView(View):

    def get(self, request):
        return render(request, "403.html", {'page_title': build_page_title('403 FLAGRANT SYSTEM ERROR'), 'page_keywords': '', 'website': ''})


class PageNotFoundView(View):

    def get(self, request):
        return render(request, "404.html", {'page_title': build_page_title('404 FLAGRANT SYSTEM ERROR'), 'page_keywords': '', 'website': ''})


class ServerErrorView(View):

    def get(self, request):
        return render(request, "500.html", {'page_title': build_page_title('500 FLAGRANT SYSTEM ERROR'), 'page_keywords': '', 'website': ''})


class AboutView(View):

    def get(self, request):
        return render(request, "about.html", {'page_title': build_page_title('About'), 'page_keywords': '', 'website': ''})


class ArticlesView(View):

    def get(self, request, category=None, tag=None, year=None, month=None, page=0):
        filter = { 'date_published__lte': timezone.now() }
        order_by = [ '-date_published' ]

        # Display unpublished articles to admin users
        if request.user.is_authenticated() and request.user.has_perm('lukexor_me.change_article'):
            filter = {}
            order_by = [ '-created', '-date_published' ]

        all_articles = models.Article.objects.filter(**filter).order_by(*order_by)
        articles_archive = datify_archive(all_articles)

        limit = settings.PAGE_LIMITS['articles']
        offset = get_page_offset(page, limit)

        filtered_articles = None
        next_page_url = None
        prev_page_url = None
        prev_page = get_prev_page(page)

        if category:
            unslugified_category = category.replace('-', ' ')
            filtered_articles = all_articles.filter(category__name=unslugified_category)

            next_page = get_next_page(page, limit, filtered_articles.count())

            if next_page:
                next_page_url = reverse_lazy('article_category_page', args=[category, next_page])

            if prev_page > 0:
                prev_page_url = reverse_lazy('article_category_page', args=[category, prev_page])
            elif prev_page == 0:
                prev_page_url = reverse_lazy('article_category', args=[category])
        elif tag:
            unslugified_tag = tag.replace('-', ' ')
            filtered_articles = all_articles.filter(tags__name=unslugified_tag)

            next_page = get_next_page(page, limit, filtered_articles.count())

            if next_page:
                next_page_url = reverse_lazy('article_tag_page', args=[tag, next_page])

            if prev_page > 0:
                prev_page_url = reverse_lazy('article_tag_page', args=[tag, prev_page])
            elif prev_page == 0:
                prev_page_url = reverse_lazy('article_tag', args=[tag])
        elif year:
            if month:
                min_date = datetime.datetime(int(year), int(month), 01)
                if int(month) == 12:
                    max_date = datetime.datetime(int(year) + 1, 01, 01) - datetime.timedelta(days = 1)
                else:
                    max_date = datetime.datetime(int(year), int(month) + 1, 01) - datetime.timedelta(days = 1)

                filtered_articles = all_articles.filter(created__gte=min_date).filter(created__lte=max_date)

                next_page = get_next_page(page, limit, filtered_articles.count())

                if next_page:
                    next_page_url = reverse_lazy('articles_date_page', args=[year, month, next_page])

                if prev_page > 0:
                    prev_page_url = reverse_lazy('articles_date_page', args=[year, month, prev_page])
                elif prev_page == 0:
                    prev_page_url = reverse_lazy('articles_date', args=[year, month])
            else:
                filtered_articles = all_articles.filter(created__year=int(year))

                next_page = get_next_page(page, limit, filtered_articles.count())

                if next_page:
                    next_page_url = reverse_lazy('articles_year_page', args=[year, next_page])

                if prev_page > 0:
                    prev_page_url = reverse_lazy('articles_year_page', args=[year, prev_page])
                elif prev_page == 0:
                    prev_page_url = reverse_lazy('articles_year', args=[year])
        else:
            filtered_articles = all_articles

            next_page = get_next_page(page, limit, filtered_articles.count())

            if next_page:
                next_page_url = reverse_lazy('articles_page', args=[next_page])

            if prev_page > 0:
                prev_page_url = reverse_lazy('articles_page', args=[prev_page])
            elif prev_page == 0:
                prev_page_url = reverse_lazy('articles')

        articles = filtered_articles[offset:offset + limit]

        return render(request, "articles.html", {
            'articles': articles,
            'archive': articles_archive,
            'categories': get_article_categories(),
            'comments_enabled': settings.COMMENTS_ENABLED,
            'next_page_url': next_page_url,
            'page_title': build_page_title('Articles'),
            'page_description': "Articles :: " + settings.STRINGS['full_name'],
            'prev_page_url': prev_page_url,
            'tags': get_article_tags(),
            'page_keywords': '',
            'website': '',
        })


class ContactView(View):

    @method_decorator(check_honeypot)
    def post(self, request):
        form = forms.ContactForm(request.POST, auto_id = "field-%s")

        if form.is_valid():
            name = form.cleaned_data['name']
            sender = "%s <%s>" % (name, form.cleaned_data['email'])
            message = form.cleaned_data['message']
            recipients = [settings.STRINGS['admin_email']]

            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            subject = "New message from %s on lukeworks.tech at: %s" % (name, date)
            message = message + "\n\nAt: " + date

            email = EmailMessage(subject, message, sender, recipients, headers={'Reply-To': sender})
            email.send()

            return HttpResponseRedirect('%s' % (reverse_lazy('thanks')))
        else:
            return render(request, "contact.html", {'form': form, 'page_title': build_page_title('Contact'), 'page_keywords': '', 'website': ''})

    def get(self, request):

        form = forms.ContactForm(auto_id = "field-%s")

        return render(request, "contact.html", {'form': form, 'page_title': build_page_title('Contact'), 'page_keywords': '', 'website': ''})


class SearchArticlesView(View):

    @method_decorator(check_honeypot)
    def post(self, request):
        search_term = None

        if ('search_term' in request.POST) and request.POST['search_term'].strip():
            search_term = request.POST['search_term'].strip()
            search_url = reverse_lazy('article_search', args=[search_term])

            return HttpResponseRedirect('%s' % (search_url))

    def get(self, request, page=0, query=None):
        limit = settings.PAGE_LIMITS['search']
        offset = get_page_offset(page, limit)

        next_page_url = None
        prev_page_url = None
        prev_page = get_prev_page(page)
        search = SiteSearch()
        search_results = None
        filtered_results = None
        results_string = ''

        filter = { 'date_published__lte': timezone.now() }
        order_by = [ '-date_published' ]

        # Display unpublished articles to admin users
        if request.user.is_authenticated() and request.user.has_perm('lukexor_me.change_article'):
            filter = {}
            order_by = [ '-created', '-date_published' ]

        all_articles = models.Article.objects.filter(**filter).order_by(*order_by)

        if query:
            search_query = search.get_query(query, ['title', 'body', 'author__full_name', 'tags__name', 'category__name'])

            search_results = models.Article.objects.filter(search_query).filter(**filter).order_by(*order_by).distinct()

            next_page = get_next_page(page, limit, search_results.count())

            if next_page:
                next_page_url = reverse_lazy('article_search_page', args=[query, next_page])

            if prev_page > 0:
                prev_page_url = reverse_lazy('article_search_page', args=[query, prev_page])
            elif prev_page == 0:
                prev_page_url = reverse_lazy('article_search', args=[query])

            filtered_results = search_results[offset:offset + limit]

        results_string = create_results_string(search_results.count(), offset, limit)

        return render(request, "search.html", {
            'archive': datify_archive(all_articles),
            'articles': filtered_results,
            'comments_enabled': settings.COMMENTS_ENABLED,
            'next_page_url': next_page_url,
            'prev_page_url': prev_page_url,
            'query': query,
            'results_string': results_string,
            'page_keywords': '',
            'website': '',
        })

class HomeView(View):

    def get(self, request):
        return render(request, "index.html", {
            'page_title': build_page_title(settings.STRINGS['site_subtitle']),
            'page_description': settings.STRINGS['homepage_description'],
            'page_keywords': settings.STRINGS['homepage_keywords'],
            'website': '',
        })


class ProjectsView(View):

    def get(self, request, page=0, tag=None, year=None, month=None):
        filter = { 'date_published__lte': timezone.now() }
        order_by = [ '-date_published' ]

        if request.user.is_authenticated() and request.user.has_perm('lukexor_me.change_article'):
            filter = {}
            order_by = [ '-created', '-date_published' ]

        all_projects = models.Project.objects.filter(**filter).order_by(*order_by)

        limit = settings.PAGE_LIMITS['projects']
        offset = get_page_offset(page, limit)
        prev_page = get_prev_page(page)

        filtered_projects = None
        next_page_url = None
        prev_page_url = None

        if tag:
            unslugified_tag = tag.replace('-', ' ')
            filtered_projects = all_projects.filter(tags__name=unslugified_tag)

            next_page = get_next_page(page, limit, filtered_projects.count())

            if next_page:
                next_page_url = reverse_lazy('project_tag_page', args=[tag, next_page])

            if prev_page > 0:
                prev_page_url = reverse_lazy('project_tag_page', args=[tag, prev_page])
            elif prev_page == 0:
                prev_page_url = reverse_lazy('projtect_tag', args=[tag])
        else:
            filtered_projects = all_projects

            next_page = get_next_page(page, limit, filtered_projects.count())

            if next_page:
                next_page_url = reverse_lazy('projects_page', args=[next_page])

            if prev_page > 0:
                prev_page_url = reverse_lazy('projects_page', args=[prev_page])
            elif prev_page == 0:
                prev_page_url = reverse_lazy('projects')

        projects = filtered_projects[offset:offset + limit]

        return render(request, "projects.html", {
            'comments_enabled': settings.COMMENTS_ENABLED,
            'next_page_url': next_page_url,
            'page_title': build_page_title('Projects'),
            'page_description': "Projects :: " + settings.STRINGS['full_name'],
            'prev_page_url': prev_page_url,
            'projects': projects,
            'tags': get_project_tags(),
            'page_keywords': '',
            'website': '',
        })


class ThanksView(View):

    def get(self, request):
        return render(request, "thanks.html", {'page_title': build_page_title('Thanks'), 'page_keywords': '', 'website': ''})


class PermalinkView(View):

    @method_decorator(check_honeypot)
    def post(self, request, year=None, month=None, permalink_title=None):
        form = forms.CommentForm(request.POST, auto_id = "field-%s")

        found_post = models.Project.objects.filter(date_published__lte=timezone.now(), permalink_title=permalink_title).first()
        post_type = 'project'
        permalink_url = 'project_permalink'

        if not found_post:
            found_post = models.Article.objects.filter(date_published__lte=timezone.now(), permalink_title=permalink_title).first()
            post_type = 'article'
            permalink_url = 'article_permalink'

        if found_post:
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email'].lower().strip()
                website = form.cleaned_data['website']
                message = form.cleaned_data['message']
                remember_me = form.cleaned_data['remember_me']

                md5_email = hashlib.md5(email).hexdigest()

                user = models.CustomUser.objects.get_or_create(
                    email = email,
                    defaults = {
                        'full_name': name,
                        'website': website,
                        'gravatar': settings.URLS['gravatar'] % (md5_email)
                    },
                )

                if user:
                    if post_type == 'article':
                        comment = models.Comment.objects.create(
                            user = user[0],
                            article = found_post,
                            body = message,
                        )
                    elif post_type == 'project':
                        comment = models.Comment.objects.create(
                            user = user[0],
                            project = found_post,
                            body = message,
                        )

                    if comment:
                        # TODO
                        # lib.cache.expire_view_cache(permalink_url, [found_post.permalink_title])

                        if remember_me:
                            request.session['comment_remember'] = {
                                'name': name,
                                'email': email,
                                'website': website,
                                'remember_me': remember_me,
                            }
                        else:
                            request.session['comment_remember'] = None

                        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        sender = "%s <%s>" %(name, email)
                        recipients = [settings.STRINGS['admin_email']]
                        subject = "New comment from %s on lukeworks.tech for %s at: %s" % (name, found_post.title, date)
                        message = message + "\n\nAt: " + date

                        email = EmailMessage(subject, message, sender, recipients, headers={'Reply-To': sender})
                        email.send()

                        comment_count = found_post.comment_set.count()
                        year = found_post.date_published.strftime('%Y')
                        month = found_post.date_published.strftime('%m')
                        url = reverse_lazy(permalink_url, args=[year, month, found_post.permalink_title])

                        return HttpResponseRedirect("%s#comment-%d" % (url, comment_count))
                    else:
                        form.add_error(None, "An error occurred posting your comment.")
                else:
                    form.add_error(None, "There was an error posting your comment.")

                if post_type == 'article':
                    return article_view(request, found_post, form)
                else:
                    return project_view(request, found_post, form)
            else:
                if post_type == 'article':
                    return article_view(request, found_post, form)
                else:
                    return project_view(request, found_post, form)
        else:
            raise Http404

    def get(self, request, year=None, month=None, permalink_title=None):
        form = forms.CommentForm(auto_id = "field-%s")
        filter = {
            'date_published__lte': timezone.now(),
            'permalink_title': permalink_title,
        }

        if request.user.is_authenticated() and request.user.has_perm('lukexor_me.change_article'):
            filter = { 'permalink_title': permalink_title }

        session_data = request.session.get('comment_remember', None)
        if session_data:
            form.fields['name'].initial = session_data['name']
            form.fields['email'].initial = session_data['email']
            form.fields['website'].initial = session_data['website']
            form.fields['remember_me'].initial = session_data['remember_me']

        found_project = models.Project.objects.filter(**filter).first()
        if found_project:
            return project_view(request, found_project, form)

        found_article = models.Article.objects.filter(**filter).first()
        if found_article:
            return article_view(request, found_article, form)
        else:
            raise Http404
