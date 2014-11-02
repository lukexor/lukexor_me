from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import *

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    # url(r'articles/$', ArticlesView.as_view(), name='articles'),
    url(r'articles/$', HomeView.as_view(), name='articles'),
    # url(r'(?P<article_title>\w+)/$', HomeView.as_view()),
    # url(r'^projects/$', ProjectsView.as_view(), name='projects'),
    url(r'projects/$', HomeView.as_view(), name='projects'),
    # url(r'^(?P<project_title>\w+)/$', HomeView.as_view()),
    # url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'about/$', HomeView.as_view(), name='about'),
    # url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'contact/$', HomeView.as_view(), name='contact'),
    url(r'^subscribe/$', HomeView.as_view(), name='subscribe'),

    url(r'^admin/', include(admin.site.urls), name='admin'),
)
