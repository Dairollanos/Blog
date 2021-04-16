from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/ultimos_posts.html')
def show_ultimos_posts(contador=5):
    ultimos_posts = Post.published.order_by('-publicado')[:contador]
    return {'ultimos_posts': ultimos_posts}

@register.simple_tag
def get_post_mas_comentado(count=5):
    return Post.published.annotate(total_comentarios=Count('comentarios')).order_by('-total_comentarios')[:count]