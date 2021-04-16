from django.contrib import admin
from .models import Post, Comentario

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'autor', 'publicado', 'status')
    list_filter = ('status', 'creado', 'publicado', 'autor')
    search_fields = ('titulo', 'body')
    prepopulated_fields = {'slug': ('titulo',)}
    raw_id_fields = ('autor',)
    date_hierarchy = 'publicado'
    ordering = ('status', 'publicado')

@admin.register(Comentario)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'post', 'creado', 'activo')
    list_filter = ('activo', 'creado', 'actualizado')
    search_fields = ('nombre', 'email', 'body')