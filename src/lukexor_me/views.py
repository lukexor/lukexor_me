from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View


class HomeView(View):

    def get(self, request):
        return render(request, "index.html")


class ArticlesView(View):

    def get(self, request):
        return render(request, "articles.html")


class ProjectsView(View):

    def get(self, request):
        return render(request, "projects.html")


class AboutView(View):

    def get(self, request):
        return render(request, "about.html")


class ContactView(View):

    def get(self, request):
        return render(request, "contact.html")
