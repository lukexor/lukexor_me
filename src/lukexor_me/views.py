from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.views.generic import View
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
import logging

logger = logging.getLogger(__name__)

def build_page_title(title):
    return '%s :: %s' % (title, settings.STRINGS['full_name'])


class HomeView(View):

    def get(self, request):
        return render(request, "index.html", {'page_title': build_page_title(settings.STRINGS['site_subtitle'])})


class ArticlesView(View):

    def get(self, request):
        return render(request, "articles.html", {'page_title': build_page_title('Articles')})


class ProjectsView(View):

    def get(self, request):
        return render(request, "projects.html", {'page_title': build_page_title('Projects')})


class TitleView(View):

    def get(self, request, title=None):
        title=None
        if title:
            return render(request, "%s.html" % (title), {'page_title': build_page_title(title)})
        else:
            raise Http404


class AboutView(View):

    def get(self, request):
        return render(request, "about.html", {'page_title': build_page_title('About')})


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
                recipients, headers = {'Reply-To': sender})

            email.send()

            return HttpResponseRedirect('/thanks/')
        else:
            return render(request, "contact.html", {'form': form, 'page_title': build_page_title('Contact')})

    def get(self, request):

        form = ContactForm()

        return render(request, "contact.html", {'form': form, 'page_title': build_page_title('Contact')})


class ThanksView(View):

    def get(self, request):
        return render(request, "thanks.html", {'page_title': build_page_title('Thanks')})
