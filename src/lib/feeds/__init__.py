from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.utils.feedgenerator import Atom1Feed
from django.utils import timezone
from lukexor_me import models, settings
import markdown_deux

class CustomAtom1Feed(Atom1Feed):
    mime_type = 'application/xml'
    
    def add_item_elements(self, handler, item):
        super(CustomAtom1Feed, self).add_item_elements(handler, item)
        handler.addQuickElement(u"content", item['content'], {"type": "html"})

class Feed(Feed):
    feed_type = CustomAtom1Feed

    title = "Lucas Petherbridge"
    subtitle = settings.STRINGS['homepage_description']
    description = settings.STRINGS['homepage_description']

    author_name = settings.STRINGS['full_name']
    author_email = settings.STRINGS['plain_email']

    link = reverse_lazy('articles')
    feed_url = reverse_lazy('feed')

    categories = models.Category.objects.all()
    feed_copyright = settings.STRINGS['copyright']


    def items(self):
        return models.Article.objects.filter(date_published__lte=timezone.now()).order_by('-created')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown_deux.markdown(item.summary(), "trusted")

    def item_pubdate(self, item):
        return item.created

    def item_updateddate(self, item):
        return item.updated

    def item_extra_kwargs(self, item):
        return {
            'content': markdown_deux.markdown(item.body, "trusted"),
        }
