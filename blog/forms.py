from django import forms
from .models import Comentario
from .models import Post

class EmailPostForm(forms.Form):
    para = forms.EmailField()
    comentarios = forms.CharField(required=False, widget=forms.Textarea)

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('body',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'body', 'tags']

