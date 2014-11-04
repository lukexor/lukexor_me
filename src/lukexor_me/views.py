from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.views.generic import View
from django.core.mail import send_mail
from lukexor_me.forms import ContactForm


class HomeView(View):

    def get(self, request):
        return render(request, "index.html")


class ArticlesView(View):

    def get(self, request):
        return render(request, "articles.html")


class ProjectsView(View):

    def get(self, request):
        return render(request, "projects.html")


class TitleView(View):

    def get(self, request, title=None):
        title=None
        if title:
            return render(request, "%s.html" % (title))
        else:
            raise Http404


class AboutView(View):

    def get(self, request):
        return render(request, "about.html")


class ContactView(View):

    def get(self, request):
        if request.method == 'POST':
            form = ContactForm(request.POST)

            if form.is_valid():
                name = form.cleaned_data['name']
                sender = form.cleaned_data['email']
                message = form.cleaned_data['message']
                recipients = ['lukexor@gmail.com']

                subject = "New message from %s on lukexor.me" % (name)

                send_mail(subject, message, sender, recipients)

                return HttpResponseRedirect('/thanks/')
        else:
            form = ContactForm()

        return render(request, "contact.html", {'form': form})
