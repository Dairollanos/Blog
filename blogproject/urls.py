"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from Usuarios.views import login_view, logout_view, registrar_view, perfil_view
from django.contrib.auth import views as auth_views

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace = "blog")),
    path('login/', login_view, name = "login"),
    path('logout/', logout_view, name = "logout"),
    path('registrar/', registrar_view, name = "registrar"),
    path('perfil/', perfil_view, name="perfil"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('cambiar_contraseña/',auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('cambiar_contraseña_hecho')),name='cambiar_contraseña'),
    path('cambiar_contraseña/hecho/',auth_views.PasswordChangeDoneView.as_view(),name='cambiar_contraseña_hecho'),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
