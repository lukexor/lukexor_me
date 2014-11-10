from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.views.generic import View
from django.core.mail import EmailMessage
from django.conf import settings
from lib.site_search import SiteSearch
from .forms import ContactForm
from .models import Article, Project

import logging

logger = logging.getLogger(__name__)


def build_page_title(title):
    return '%s :: %s' % (title, settings.STRINGS['full_name'])


class AboutView(View):

    def get(self, request):
        return render(request, "about.html", {'page_title': build_page_title('About')})


class ArticlesView(View):

    def get(self, request):
        curr_page = 0
        prev_page = None
        next_page = None
        offset = 0
        limit = settings.PAGE_LIMITS['articles']

        articles = None

        if ('p' in request.GET) and request.GET['p'].strip():
            curr_page = int(request.GET['p'])

            offset = curr_page * limit

        articles = Article.objects.all().order_by('-created')

        if articles.count() > offset + limit:
            next_page = curr_page + 1

        if curr_page > 0:
            prev_page = curr_page - 1

        articles = articles[offset:offset + limit]

        return render(request, "articles.html", {
            'page_title': build_page_title('Articles'),
            'articles': articles,
            'prev_page': prev_page,
            'next_page': next_page,
        })


class ContactView(View):

    def post(self, request):
        form = ContactForm(request.POST)

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

        form = ContactForm()

        return render(request, "contact.html", {'form': form, 'page_title': build_page_title('Contact')})


class HomeView(View):

    def get(self, request):
        query_string = ''
        found_articles = None
        found_projects = None
        limit = settings.PAGE_LIMITS['search']

        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']

            search = SiteSearch()
            article_query = search.get_query(query_string, ['title', 'body', 'tags__name', 'category__name'])  # TODO Add Tags/Category search
            project_query = search.get_query(query_string, ['title', 'description', 'client'])

            offset = 0 # TODO Add pagination
            if ('p' in request.GET) and request.GET['p'].strip():
                page = request.GET['p']

                offset = int(page) * limit

            found_projects = Project.objects.filter(project_query).order_by('-created').distinct()[offset:offset + limit]
            found_articles = Article.objects.filter(article_query).order_by('-created').distinct()[offset:offset + limit]

            total_count = found_projects.count() + found_articles.count()

            count_string = ""

            # 2 * limit is so we can have exactly limit of articles and projects
            if (total_count > (2 * limit)):
                count_string += "%d" % (offset + 1)

                count_string += " - %d of %d" % (2 * (limit + offset), total_count)
            else:
                count_string += "%d" % (total_count)

            count_string += " result"

            if (total_count != 1):
                count_string += "s"

            return render(request, "search.html", {
                'query_string': query_string,
                'projects': found_projects,
                'articles': found_articles,
                'count_string': count_string,
            })
        else:
            return render(request, "index.html", {'page_title': build_page_title(settings.STRINGS['site_subtitle'])})


class ProjectsView(View):

    def get(self, request):
        curr_page = 0
        next_page = None
        prev_page = None
        offset = 0
        limit = settings.PAGE_LIMITS['projects']

        projects = None

        if ('p' in request.GET) and request.GET['p'].strip():
            curr_page = int(request.GET['p'])

            offset = curr_page * limit

        projects = Project.objects.all().order_by('-created')

        if projects.count() > offset + limit:
            next_page = curr_page + 1

        if curr_page > 0:
            prev_page = curr_page - 1

        projects = projects[offset:offset + limit]

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
        title = None
        if title:
            return render(request, "%s.html" % (title), {'page_title': build_page_title(title)})
        else:
            raise Http404
