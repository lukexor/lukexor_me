from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page
from lukexor_me import views, settings
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

    url(r'^sitemap\.xml$', cache_page(settings.CACHE_TIMES['post'])(sitemap), {'sitemaps': sitemaps}, name='sitemap'),

    url(r'^articles/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='articles'),
    url(r'^articles/page/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='articles_page'),
    url(r'^articles/tag/(?P<tag>[\w-]+)/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='article_tag'),
    url(r'^articles/tag/(?P<tag>[\w-]+)/page/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='article_tag_page'),
    url(r'^articles/category/(?P<category>[\w-]+)/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='article_category'),
    url(r'^articles/category/(?P<category>[\w-]+)/page/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='article_category_page'),
    url(r'^articles/search/$', cache_page(settings.CACHE_TIMES['post'])(views.SearchArticlesView.as_view()), name='article_search_post'),
    url(r'^articles/search/(?P<query>[\w-]+)$', cache_page(settings.CACHE_TIMES['post'])(views.SearchArticlesView.as_view()), name='article_search'),
    url(r'^articles/search/(?P<query>[\w-]+)/page/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.SearchArticlesView.as_view()), name='article_search_page'),
    url(r'^articles/(?P<year>[\d]{4})/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='articles_year'),
    url(r'^articles/(?P<year>[\d]{4})/page/(?P<page>[\d]{1,})$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='articles_year_page'),
    url(r'^articles/(?P<year>[\d]{4})/(?P<month>[\d]{2})/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='articles_date'),
    url(r'^articles/(?P<year>[\d]{4})/(?P<month>[\d]{2})/page/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.ArticlesView.as_view()), name='articles_date_page'),
    url(r'^articles/(?P<year>[\d]{4})/(?P<month>[\d]{2})/(?P<permalink_title>[\w-]+)/$', cache_page(settings.CACHE_TIMES['post'])(views.PermalinkView.as_view()), name='article_permalink'),
    url(r'^articles/(?P<permalink_title>[\w-]+)/$', cache_page(settings.CACHE_TIMES['post'])(views.PermalinkView.as_view()), name='DEPRECATED_article_permalink'),

    url(r'^projects/$', cache_page(settings.CACHE_TIMES['post'])(views.ProjectsView.as_view()), name='projects'),
    url(r'^projects/page/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.ProjectsView.as_view()), name='projects_page'),
    url(r'^projects/tag/(?P<tag>[\w-]+)/$', cache_page(settings.CACHE_TIMES['post'])(views.ProjectsView.as_view()), name='project_tag'),
    url(r'^projects/tag/(?P<tag>[\w-]+)/page/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.ProjectsView.as_view()), name='project_tag_page'),
    url(r'^projects/(?P<year>[\d]{4})/(?P<month>[\d]{2})/$', cache_page(settings.CACHE_TIMES['post'])(views.ProjectsView.as_view()), name='projects_date'),
    url(r'^projects/(?P<year>[\d]{4})/(?P<month>[\d]{2})/page/(?P<page>[\d]{1,})/$', cache_page(settings.CACHE_TIMES['post'])(views.ProjectsView.as_view()), name='projects_date_page'),
    url(r'^projects/(?P<year>[\d]{4})/(?P<month>[\d]{2})/(?P<permalink_title>[\w-]+)/$', cache_page(settings.CACHE_TIMES['post'])(views.PermalinkView.as_view()), name='project_permalink'),

    url(r'^about/$', cache_page(settings.CACHE_TIMES['static'])(views.AboutView.as_view()), name='about'),
    url(r'^contact/$', cache_page(settings.CACHE_TIMES['static'])(views.ContactView.as_view()), name='contact'),
    url(r'^thanks/$', cache_page(settings.CACHE_TIMES['static'])(views.ThanksView.as_view()), name='thanks'),
    url(r'^feed/$', cache_page(settings.CACHE_TIMES['post'])(feeds.Feed()), name='feed'),

    url(r'^siteadmin/doc/', include('django.contrib.admindocs.urls'), name='admin_doc'),
    url(r'^siteadmin/', include(admin.site.urls), name='admin')
)
