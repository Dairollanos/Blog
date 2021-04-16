from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                                self).get_queryset()\
                                .filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    titulo = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publicado')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    body = models.TextField()
    publicado = models.DateTimeField(default=timezone.now)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    tags = TaggableManager() # Administrador de tags
    objects = models.Manager() # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ('-publicado',)

    def save(self, *args, **kwargs):
            if not self.id:
                self.slug = slugify(self.titulo)

            super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('blog:post_detalle', args=[self.publicado.year,
                                                    self.publicado.month,
                                                    self.publicado.day, self.slug])

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    nombre = models.ForeignKey(User, on_delete=models.CASCADE, related_name="autor_comentarios")
    email = models.EmailField()
    body = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ('creado',)
    def __str__(self):
        return f'Commentario de {self.nombre} en {self.post}'