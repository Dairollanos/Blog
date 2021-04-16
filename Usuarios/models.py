from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    biografia = models.TextField(default="No biografia")
    avatar = models.ImageField(upload_to='profiles', default="no-profile-picture.jpg")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.usuario.username


    @receiver(post_save, sender=User)
    def post_save_create_perfil(sender, instance, created, **kwargs):
        if created:
            Perfil.objects.create(usuario = instance)
