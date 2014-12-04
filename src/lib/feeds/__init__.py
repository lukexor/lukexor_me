from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.utils.feedgenerator import Atom1Feed
from django.conf import settings
from lukexor_me import models

class Feed(Feed):
    feed_type = Atom1Feed

    title = "Lucas Petherbridge"
    subtitle = settings.STRINGS['homepage_description']
    description = settings.STRINGS['homepage_description']

    author_name = settings.STRINGS['full_name']
    author_email = settings.STRINGS['plain_email']
    author_link = reverse_lazy('about')

    link = reverse_lazy('articles')
    feed_url = reverse_lazy('feed')

    categories = models.Category.objects.all()
    feed_copyright = settings.STRINGS['copyright']


    def items(self):
        return models.Article.objects.filter(is_published=True).order_by('-date_published')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary()

    def item_pubdate(self, item):
        return item.date_published

    def item_updateddate(self, item):
        return item.updated
