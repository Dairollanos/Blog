from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Perfil



class RegistrarUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class PerfilForm(forms.ModelForm):
    avatar = forms.ImageField(label=('Avatar'),required=False, error_messages = {'invalid':("Archivos de imagenes solamente")}, widget=forms.FileInput)
    class Meta:
        model = Perfil
        fields = ['avatar', 'biografia']


