from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page
from . import views
from lib import feeds, site_maps

sitemaps = {
    'static': site_maps.StaticSitemap,
    'articles': site_maps.ArticleSitemap,
    'article_tags': site_maps.ArticleTagSiteMap,
    'article_categories': site_maps.ArticleCategorySiteMap,
    'projects': site_maps.ProjectSitemap,
    'project_tags': site_maps.ProjectTagSiteMap,
}

urlpatterns = patterns(
    '',
    url(r'^$', cache_page(settings.CACHE_TIMES['static'])(views.HomeView.as_view()), name='home'),
    url(r'^articles/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='articles'),
    url(r'^projects/$', cache_page(settings.CACHE_TIMES['post'])(views.ProjectsView.as_view()), name='projects'),
    url(r'^about/$', cache_page(settings.CACHE_TIMES['static'])(views.AboutView.as_view()), name='about'),
    url(r'^contact/$', cache_page(settings.CACHE_TIMES['static'])(views.ContactView.as_view()), name='contact'),
    url(r'^search/$', cache_page(settings.CACHE_TIMES['post'])(views.SearchArticlesView.as_view()), name='search'),
    url(r'^thanks/$', cache_page(settings.CACHE_TIMES['static'])(views.ThanksView.as_view()), name='thanks'),
    url(r'^feed/$', feeds.Feed(), name='feed'),

    url(r'^articles/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='articles_by_page'),
    url(r'^projects/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.ProjectsView.as_view()), name='projects_by_page'),

    url(r'^search/(?P<query>[\w\s-]+)/$', cache_page(settings.CACHE_TIMES['post'])(views.SearchArticlesView.as_view()), name='search_by_term'),
    url(r'^search/(?P<query>[\w\s-]+)/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.SearchArticlesView.as_view()), name='search_by_page'),

    url(r'^category/(?P<category>[\w-]+)/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='category_search'),
    url(r'^category/(?P<category>[\w-]+)/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='category_search_by_page'),

    url(r'^tag/(?P<tag>[\w-]+)/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='tag_search'),
    url(r'^tag/(?P<tag>[\w-]+)/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='tag_search_by_page'),

    url(r'^projects/tag/(?P<tag>[\w-]+)/$', cache_page(settings.CACHE_TIMES['post'])(views.ProjectsView.as_view()), name='project_tag_search'),
    url(r'^projects/tag/(?P<tag>[\w-]+)/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.ProjectsView.as_view()), name='project_tag_search_by_page'),

    url(r'^(?P<year>[\d]{4})/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='year_search'),
    url(r'^(?P<year>[\d]{4})/(?P<month>[\d]{2})/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='month_search'),

    url(r'^tinymce/', include('tinymce.urls'), name='tinymce'),
    url(r'^siteadmin/doc/', include('django.contrib.admindocs.urls'), name='admin_doc'),
    url(r'^siteadmin/', include(admin.site.urls), name='admin'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    url(r'^(?P<permalink_title>[\w-]+)/$', cache_page(settings.CACHE_TIMES['post'])(views.PermalinkView.as_view()), name='permalink'),
)
