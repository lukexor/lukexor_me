from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
from lib.feeds import Feed

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^articles/$', views.ArticlesView.as_view(), name='articles'),
    url(r'^projects/$', views.ProjectsView.as_view(), name='projects'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^search/$', views.SearchArticlesView.as_view(), name='search'),
    url(r'^thanks/$', views.ThanksView.as_view(), name='thanks'),
    url(r'^feed/$', Feed(), name='feed'),

    url(r'^articles/(?P<page>[\d]{1,})/$', views.ArticlesView.as_view(), name='articles_by_page'),
    url(r'^search/(?P<query>[\w\s-]+)/$', views.SearchArticlesView.as_view(), name='search_by_term'),
    url(r'^search/(?P<query>[\w\s-]+)/(?P<page>[\d]{1,})/$', views.SearchArticlesView.as_view(), name='search_by_page'),

    url(r'^category/(?P<category>[\w-]+)/$', views.ArticlesView.as_view(), name='category_search'),
    url(r'^category/(?P<category>[\w-]+)/(?P<page>[\d]{1,})/$', views.ArticlesView.as_view(), name='category_search_by_page'),

    url(r'^tag/(?P<tag>[\w-]+)/$', views.ArticlesView.as_view(), name='tag_search'),
    url(r'^tag/(?P<tag>[\w-]+)/(?P<page>[\d]{1,})/$', views.ArticlesView.as_view(), name='tag_search_by_page'),

    url(r'^projects/tag/(?P<tag>[\w-]+)/$', views.ProjectsView.as_view(), name='project_tag_search'),
    url(r'^projects/tag/(?P<tag>[\w-]+)/(?P<page>[\d]{1,})/$', views.ProjectsView.as_view(), name='project_tag_search_by_page'),

    url(r'^(?P<year>[\d]{4})/$', views.ArticlesView.as_view(), name='year_search'),
    url(r'^(?P<year>[\d]{4})/(?P<month>[\d]{2})/$', views.ArticlesView.as_view(), name='month_search'),

    url(r'^(?P<permalink_title>[\w-]+)/$', views.PermalinkView.as_view(), name='permalink'),

    url(r'^tinymce/', include('tinymce.urls'), name='tinymce'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
)
