from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import *

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^articles/$', ArticlesView.as_view(), name='articles'),

    url(r'^projects/$', ProjectsView.as_view(), name='projects'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^thanks/$', ThanksView.as_view(), name='thanks'),
    url(r'^subscribe/$', HomeView.as_view(), name='subscribe'),
    url(r'^articles/(?P<year>\d{4})/$', HomeView.as_view()),
    url(r'^(?P<title>\w+)/$', TitleView.as_view(), name='permalink'),


    url(r'^admin/', include(admin.site.urls), name='admin'),
)
