from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from lukexor_me import models

class ArticleSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return models.Article.objects.filter(is_published=True)

    def lastmod(self, item):
        return item.updated

class ArticleTagSiteMap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return models.Tag.objects.filter(article__isnull=False).distinct()

    def location(self, item):
        name = slugify(item.name.lower())
        return reverse('tag_search', args=[name])

class ArticleCategorySiteMap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return models.Category.objects.filter(article__isnull=False).distinct()

    def location(self, item):
        name = slugify(item.name.lower())
        return reverse('category_search', args=[name])

class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return models.Project.objects.filter(is_published=True)

    def lastmod(self, item):
        return item.updated

class ProjectTagSiteMap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return models.Tag.objects.filter(project__isnull=False).distinct()

    def location(self, item):
        name = slugify(item.name.lower())
        return reverse('project_tag_search', args=[name])

class StaticSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return ['articles', 'projects', 'about', 'contact', 'feed']

    def location(self, item):
        return reverse(item)
