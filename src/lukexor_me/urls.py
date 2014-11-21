from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
from lib.feeds import Feed

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^articles/$', views.ArticlesView.as_view(), name='articles'),
    url(r'^projects/$', views.ProjectsView.as_view(), name='projects'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^thanks/$', views.ThanksView.as_view(), name='thanks'),
    url(r'^feed/$', Feed(), name='feed'),
    url(r'^(?P<title>[\w-]+)/$', views.TitleView.as_view(), name='permalink'),

    url(r'^tinymce/', include('tinymce.urls'), name='tinymce'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
)
