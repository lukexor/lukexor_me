from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.decorators import method_decorator
from lib.site_search import SiteSearch
from honeypot.decorators import check_honeypot
from . import forms, models

import logging, datetime, hashlib, re

handler400 = 'lukexor_me.views.BadRequestView'
handler403 = 'lukexor_me.views.PermissionDeniedView'
handler404 = 'lukexor_me.views.PageNotFoundView'
handler500 = 'lukexor_me.views.ServerErrorView'
logger = logging.getLogger(__name__)


def build_page_title(title):
    return '%s :: %s' % (title, settings.STRINGS['full_name'])

def get_article_tags():
    tags = models.Tag.objects.filter(article__isnull=False).distinct()
    return tags

def get_project_tags():
    return models.Tag.objects.filter(project__isnull=False).distinct()

def get_article_categories():
    return models.Category.objects.filter(article__isnull=False).distinct()

def get_prev_page(page):
    if int(page) > 0:
        return int(page) - 1
    else:
        return None

def get_next_page(page, limit, count):
    if count > ( (int(page) + 1) * limit ):
        return int(page) + 1
    else:
        None

def get_page_offset(page, limit):
    return int(page) * limit

def create_results_string(count, offset, limit):
    count_string = ""

    if (count > (limit)):
        count_string += "%d" % (offset + 1)

        count_string += " - %d of %d" % (2 * (limit + offset), count)
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
    })

def article_view(request, article, form):
    return render(request, "articles.html", {
        'articles': [article],
        'categories': get_article_categories(),
        'comments_enabled': settings.COMMENTS_ENABLED,
        'form': form,
        'page_description': article.title + " :: " + article.summary(),
        'page_keywords': article.get_tags(),
        'page_title': build_page_title(article.title),
        'show_comments': True,
        'tags': get_article_tags(),
    })

class BadRequestView(View):
    def get(self, request):
        return render(request, "400.html", {'page_title': build_page_title('400 FLAGRANT SYSTEM ERROR')})

class PermissionDeniedView(View):
    def get(self, request):
        return render(request, "403.html", {'page_title': build_page_title('403 FLAGRANT SYSTEM ERROR')})

class PageNotFoundView(View):
    def get(self, request):
        return render(request, "404.html", {'page_title': build_page_title('404 FLAGRANT SYSTEM ERROR')})

class ServerErrorView(View):
    def get(self, request):
        return render(request, "500.html", {'page_title': build_page_title('500 FLAGRANT SYSTEM ERROR')})

class AboutView(View):

    def get(self, request):
        return render(request, "about.html", {'page_title': build_page_title('About')})


class ArticlesView(View):

    def get(self, request, category=None, tag=None, year=None, month=None, page=0):
        all_articles = models.Article.objects.filter(is_published=True).order_by('-date_published')

        article_dates = {}
        for article in all_articles:
            article_year = int(article.date_published.year)
            article_month = int(article.date_published.month)

            if article_year in article_dates:
                if article_month in article_dates[article_year]:
                    article_dates[article_year][article_month] += 1
                else:
                    article_dates[article_year][article_month] = 1
            else:
                article_dates[article_year] = {
                    article_month: 1
                }

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
                next_page_url = reverse_lazy('category_search_by_page', args=[category, next_page])

            if prev_page > 0:
                prev_page_url = reverse_lazy('category_search_by_page', args=[category, prev_page])
            elif prev_page == 0:
                prev_page_url = reverse_lazy('category_search', args=[category])
        elif tag:
            unslugified_tag = tag.replace('-', ' ')
            filtered_articles = all_articles.filter(tags__name=unslugified_tag)

            next_page = get_next_page(page, limit, filtered_articles.count())

            if next_page:
                next_page_url = reverse_lazy('tag_search_by_page', args=[tag, next_page])

            if prev_page > 0:
                prev_page_url = reverse_lazy('tag_search_by_page', args=[tag, prev_page])
            elif prev_page == 0:
                prev_page_url = reverse_lazy('tag_search', args=[tag])
        elif year:
            if month:
                min_date = datetime.datetime(int(year), int(month), 01)
                max_date = datetime.datetime(int(year), int(month) + 1, 01) - datetime.timedelta(days = 1)
                filtered_articles = all_articles.filter(date_published__gte=min_date).filter(date_published__lte=max_date)
            else:
                filtered_articles = all_articles.filter(date_published__year=int(year))
        else:
            filtered_articles = all_articles

            next_page = get_next_page(page, limit, filtered_articles.count())

            if next_page:
                next_page_url = reverse_lazy('articles_by_page', args=[next_page])

            if prev_page > 0:
                prev_page_url = reverse_lazy('articles_by_page', args=[prev_page])
            elif prev_page == 0:
                prev_page_url = reverse_lazy('articles')

        # No pagination for year/month pages
        if year:
            articles = filtered_articles
        else:
            articles = filtered_articles[offset:offset + limit]

        return render(request, "articles.html", {
            'articles': articles,
            'article_dates': article_dates,
            'categories': get_article_categories(),
            'comments_enabled': settings.COMMENTS_ENABLED,
            'next_page_url': next_page_url,
            'page_title': build_page_title('Articles'),
            'prev_page_url': prev_page_url,
            'tags': get_article_tags(),
        })


class ContactView(View):

    @method_decorator(check_honeypot)
    def post(self, request):
        form = forms.ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            sender = "%s <%s>" % (name, form.cleaned_data['email'])
            message = form.cleaned_data['message']
            recipients = [settings.STRINGS['admin_email']]

            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            subject = "New message from %s on lukexor.me at: %s" % (name, date)
            message = message + "\n\nAt: " + date

            email = EmailMessage(subject, message, sender, recipients, headers={'Reply-To': sender})
            email.send()

            return HttpResponseRedirect('%s' % (reverse_lazy('thanks')))
        else:
            return render(request, "contact.html", {'form': form, 'page_title': build_page_title('Contact')})

    def get(self, request):

        form = forms.ContactForm()

        return render(request, "contact.html", {'form': form, 'page_title': build_page_title('Contact')})


class SearchArticlesView(View):
    def get(self, request, page=0, query=None):
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q'].strip()
            return HttpResponseRedirect("%s" % (query_string))

        limit = settings.PAGE_LIMITS['search']
        offset = get_page_offset(page, limit)
        prev_page = get_prev_page(page)
        next_page = None
        search = SiteSearch()
        search_query = None
        search_results = None
        results_string = ''

        if query:
            search_query = search.get_query(query, ['title', 'body', 'author__first_name', 'author__last_name', 'tags__name', 'category__name'])
            search_results = models.Article.objects.filter(search_query).filter(is_published=True).order_by('-date_published').distinct()[offset:offset + limit]

            search_count = search_results.count()
            next_page = get_next_page(page, limit, search_count)

            results_string = create_results_string(search_count, offset, limit)

        return render(request, "search.html", {
            'comments_enabled': settings.COMMENTS_ENABLED,
            'query': query,
            'articles': search_results,
            'results_string': results_string,
            'prev_page': prev_page,
            'next_page': next_page,
        })

class HomeView(View):

    def get(self, request):
        return render(request, "index.html", {
            'page_title': build_page_title(settings.STRINGS['site_subtitle']),
            'page_description': settings.STRINGS['homepage_description'],
            'page_keywords': settings.STRINGS['homepage_keywords'],
        })


class ProjectsView(View):

    def get(self, request, page=0, tag=None):
        all_projects = models.Project.objects.all().order_by('-created')

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
                next_page_url = reverse_lazy('project_tag_search_by_page', args=[tag, next_page])

            if prev_page > 0:
                prev_page_url = reverse_lazy('project_tag_search_by_page', args=[tag, prev_page])
            elif prev_page == 0:
                prev_page_url = reverse_lazy('project_tag_search', args=[tag])
        else:
            filtered_projects = all_projects

            next_page = get_next_page(page, limit, filtered_projects.count())

            if next_page:
                next_page_url = reverse_lazy('projects_by_page', args=[next_page])

            if prev_page > 0:
                prev_page_url = reverse_lazy('projects_by_page', args=[prev_page])
            elif prev_page == 0:
                prev_page_url = reverse_lazy('projects')

        return render(request, "projects.html", {
            'comments_enabled': settings.COMMENTS_ENABLED,
            'next_page_url': next_page_url,
            'page_title': build_page_title('Projects'),
            'prev_page_url': prev_page_url,
            'projects': filtered_projects[offset:offset + limit],
            'tags': get_project_tags(),
        })


class ThanksView(View):

    def get(self, request):
        return render(request, "thanks.html", {'page_title': build_page_title('Thanks')})


class PermalinkView(View):

    @method_decorator(check_honeypot)
    def post(self, request, permalink_title=None):
        form = forms.CommentForm(request.POST)
        post_type = 'article'

        found_post = models.Project.objects.filter(permalink_title=permalink_title).first()
        if found_post:
            post_type = 'project'
        else:
            found_post = models.Article.objects.filter(permalink_title=permalink_title).first()

        if found_post:
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email'].lower().strip()
                website = form.cleaned_data['website']
                message = form.cleaned_data['message']
                remember_me = form.cleaned_data['remember_me']

                md5_email = hashlib.md5(email).hexdigest()

                name_separator = re.compile('[ ]')
                names = name_separator.split(name)
                first_name = names[0]
                last_name = ' '.join(names[1:])

                user = models.CustomUser.objects.get_or_create(
                    email = email,
                    defaults = {
                        'first_name': first_name,
                        'last_name': last_name,
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
                    else:
                        comment = models.Comment.objects.create(
                            user = user[0],
                            project = found_post,
                            body = message,
                        )

                    if comment:
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
                        subject = "New comment from %s on lukexor.me for %s at: %s" % (name, found_post.title, date)
                        message = message + "\n\nAt: " + date

                        email = EmailMessage(subject, message, sender, recipients, headers={'Reply-To': sender})
                        email.send()

                        comment_count = found_post.comment_set.count()
                        url = reverse_lazy('permalink', args=[found_post.permalink_title])

                        return HttpResponseRedirect("%s#comment_%d" % (url, comment_count))
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

    def get(self, request, permalink_title=None):
        form = forms.CommentForm()

        session_data = request.session.get('comment_remember', None)
        if session_data:
            form.fields['name'].initial = session_data['name']
            form.fields['email'].initial = session_data['email']
            form.fields['website'].initial = session_data['website']
            form.fields['remember_me'].initial = session_data['remember_me']

        found_project = models.Project.objects.filter(permalink_title=permalink_title).first()
        if found_project:
            return project_view(request, found_project, form)

        found_article = models.Article.objects.filter(permalink_title=permalink_title).first()
        if found_article:
            return article_view(request, found_article, form)
        else:
            raise Http404
