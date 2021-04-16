from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


from .models import Post, Comentario
from .forms import EmailPostForm, ComentarioForm, PostForm
from Usuarios.models import Perfil
from django.db.models import Count

from taggit.models import Tag

@login_required
def post_agregar_view(request): 
    form = PostForm(request.POST or None)
    if form.is_valid():
        post_obj = form.save(commit=False)
        post_obj.autor = request.user
        post_obj.save()
        form.save_m2m()
        return redirect('blog:post_lista')
 
    context = {
        'Form': form
    }
    return render(request, 'blog/crear_blog.html', context)

@login_required
def post_editar_view(request, post_id):
    post = Post.objects.get(id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post_obj = form.save(commit=False)
        post_obj.autor = request.user
        post_obj.save()
        form.save_m2m()
        return redirect('blog:post_lista')

    context = {
        'Form': form
    }
    return render(request, 'blog/crear_blog.html', context)

@login_required
def post_list(request, tag_slug=None):
    obj_lists = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        obj_lists = obj_lists.filter(tags__in=[tag])

    paginador = Paginator(obj_lists, 3)
    page = request.GET.get('page')
    try:
        posts = paginador.page(page)
    except PageNotAnInteger:
        posts = paginador.page(1)
    except EmptyPage:
        posts = paginador.page(paginador.num_pages)

    context = {
        'Posts': posts,
        'Tag': tag,
        # 'Page': page
    }
    return render(request, 'blog/lista.html', context)

@login_required
def post_email(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    user = request.user
    enviado = False
    form = EmailPostForm()
    if request.method == 'POST':
        form = EmailPostForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{user.username} recomienda que leas " f"{post.titulo}"
            message = f"Lee {post.titulo} at {post_url}\n\n" f"{user.username} opina: {cd['comentarios']}"
            send_mail(subject, message, 'dairoollanos@gmail.com',
            [cd['para']])
            enviado = True
    else:
        form = EmailPostForm()
    context = {
        'Form': form,
        'Post': post,
        'Enviado': enviado
    }
    return render(request, 'blog/email.html', context)


@login_required
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
        publicado__year=year, publicado__month=month, publicado__day=day)
    
    perfil = Perfil.objects.get(usuario=post.autor.id)

    editar = False
    if post.autor == request.user:
        editar = True

    comentarios_activos = post.comentarios.filter(activo=True)
    nuevo_comentario = None
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.post = post
            nuevo_comentario.nombre = request.user
            nuevo_comentario.email = request.user.email
            nuevo_comentario.save()
    else:
        form = ComentarioForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publicado')[:4]
    context = {
        'Post': post,
        'Form': form,
        'ComentariosActivos': comentarios_activos,
        'NuevoComentario': nuevo_comentario,
        'PostSimilares': similar_posts,
        'Editar': editar,
        'Perfil': perfil
    }
    return render(request, 'blog/detalle.html', context)