from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post

class UltimosPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_lista')
    description = 'Nuevo post de mi blog.'
    
    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.titulo

    def item_description(self, item):
     return truncatewords(item.body, 30)