from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistrarUsuarioForm, PerfilForm
from .models import Perfil
# Create your views here.

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    error_mensaje = None
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contraseña = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contraseña)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('blog:post_lista')
        else:
            error_mensaje = 'No se pudo ingresar el usuario'
    
    context = {
        'Form': form,
        'MensajeError': error_mensaje
    }
    return render(request, 'auth/login.html', context)

def registrar_view(request):
    form = RegistrarUsuarioForm()

    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:post_lista')

    context = {
        'Form': form
    }
    return render(request, 'auth/registrar.html', context)

@login_required
def perfil_view(request):
    perfil = Perfil.objects.get(usuario=request.user.id)
    form = PerfilForm(request.POST or None, request.FILES or None, instance=perfil)
    if form.is_valid():
        form.save()

    context = {
        'Form': form,
        'Perfil': perfil,
    }
    return render(request, 'auth/perfil.html', context)