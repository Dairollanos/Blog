from django.urls import path
from .views import *
from .feed import UltimosPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_lista'),
    path('crear/', post_agregar_view, name="post_agregar"),
    path('editar/<int:post_id>/', post_editar_view, name="post_editar"),
    path('tag/<slug:tag_slug>/', post_list, name='post_lista_tag'),
    # path('2/', PostListView.as_view(), name='post_lista2'),
    path('<int:post_id>/compartir/', post_email, name="enviar-email"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detalle'),
    path('feed/', UltimosPostsFeed(), name='post_feed'),
]