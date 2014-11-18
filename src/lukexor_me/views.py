from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.views.generic import View
from django.core.mail import EmailMessage
from django.conf import settings
from lib.site_search import SiteSearch
from . import forms, models

import logging

logger = logging.getLogger(__name__)


def build_page_title(title):
    return '%s :: %s' % (title, settings.STRINGS['full_name'])

def get_current_page(request):
    current_page = 0

    if ('p' in request.GET) and request.GET['p'].strip():
        current_page = int(request.GET['p'])

    return current_page

def get_prev_page(current_page):
    if current_page > 0:
        return current_page - 1
    else:
        return None

def get_next_page(current_page, limit, count):
    if count > ( (current_page + 1) * limit ):
        return current_page + 1
    else:
        None

def get_page_offset(request, limit):
    offset = get_current_page(request) * limit

    return offset

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

def project_view(request, project):
    return render(request, "projects.html", {
        'page_title': build_page_title('Projects'),
        'projects': project,
    })

def article_view(request, article):
    return render(request, "articles.html", {
        'page_title': build_page_title('Articles'),
        'articles': article,
    })


class AboutView(View):

    def get(self, request):
        return render(request, "about.html", {'page_title': build_page_title('About')})


class ArticlesView(View):

    def get(self, request, title=None):
        all_articles = models.Article.objects.all().order_by('-created')

        if title:
            return article_view(request, all_articles.filter(permalink_title=title))

        limit = settings.PAGE_LIMITS['articles']
        offset = get_page_offset(request, limit)
        curr_page = get_current_page(request)
        prev_page = get_prev_page(curr_page)
        next_page = get_next_page(curr_page, limit, all_articles.count())

        articles = all_articles[offset:offset + limit]

        return render(request, "articles.html", {
            'page_title': build_page_title('Articles'),
            'articles': articles,
            'prev_page': prev_page,
            'next_page': next_page,
        })


class ContactView(View):

    def post(self, request):
        form = forms.ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            sender = "%s <%s>" % (name, form.cleaned_data['email'])
            message = form.cleaned_data['message']
            recipients = [settings.STRINGS['admin_email']]

            subject = "New message from %s on lukexor.me" % (name)

            email = EmailMessage(subject, message, settings.STRINGS['no_reply_email'],
                                 recipients, headers={'Reply-To': sender})

            email.send()

            return HttpResponseRedirect('/thanks/')
        else:
            return render(request, "contact.html", {'form': form, 'page_title': build_page_title('Contact')})

    def get(self, request):

        form = forms.ContactForm()

        return render(request, "contact.html", {'form': form, 'page_title': build_page_title('Contact')})


class HomeView(View):

    def get(self, request):
        limit = settings.PAGE_LIMITS['search']
        offset = get_page_offset(request, limit)
        curr_page = get_current_page(request)
        prev_page = get_prev_page(curr_page)
        query_string = ''
        found_articles = None
        found_projects = None

        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']

            search = SiteSearch()
            article_query = search.get_query(query_string, ['title', 'body', 'authors__first_name', 'authors__last_name', 'tags__name', 'category__name'])
            project_query = search.get_query(query_string, ['title', 'description', 'clients__first_name', 'clients__last_name'])

            found_projects = models.Project.objects.filter(project_query).order_by('-created').distinct()[offset:offset + limit]
            found_articles = models.Article.objects.filter(article_query).order_by('-created').distinct()[offset:offset + limit]

            total_count = found_projects.count() + found_articles.count()

            next_page = get_next_page(curr_page, limit, total_count)

            # 2 * limit is so we can have exactly limit of articles and projects
            results_string = create_results_string(total_count, offset, (2 * limit))

            return render(request, "search.html", {
                'search_string': query_string,
                'projects': found_projects,
                'articles': found_articles,
                'results_string': results_string,
                'prev_page': prev_page,
                'next_page': next_page,
            })
        elif ('c' in request.GET) and request.GET['c'].strip():
            query_string = request.GET['c']

            search = SiteSearch()
            article_query = search.get_query(query_string, ['category__name'])

            found_articles = models.Article.objects.filter(article_query).order_by('-created').distinct()[offset:offset + limit]

            next_page = get_next_page(curr_page, limit, found_articles.count())

            results_string = create_results_string(found_articles.count(), offset, limit)

            return render(request, "search.html", {
                'category': query_string,
                'articles': found_articles,
                'results_string': results_string,
                'prev_page': prev_page,
                'next_page': next_page,
            })
        else:
            return render(request, "index.html", {'page_title': build_page_title(settings.STRINGS['site_subtitle'])})


class ProjectsView(View):

    def get(self, request, title=None):
        all_projects = models.Project.objects.all().order_by('-created')

        if title:
            return project_view(request, all_projects.filter(permalink_title=title))

        limit = settings.PAGE_LIMITS['projects']
        offset = get_page_offset(request, limit)
        curr_page = get_current_page(request)
        prev_page = get_prev_page(curr_page)
        next_page = get_next_page(curr_page, limit, all_projects.count())

        projects = all_projects[offset:offset + limit]

        return render(request, "projects.html", {
            'page_title': build_page_title('Projects'),
            'projects': projects,
            'next_page': next_page,
            'prev_page': prev_page,
        })


class ThanksView(View):

    def get(self, request):
        return render(request, "thanks.html", {'page_title': build_page_title('Thanks')})


class TitleView(View):

    def get(self, request, title=None):
        # Find our title
        found_project = models.Project.objects.filter(permalink_title=title)

        if found_project:
            return project_view(request, found_project)

        found_article = models.Article.objects.filter(permalink_title=title)

        if found_article:
            return article_view(request, found_article)
        else:
            raise Http404
