from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Publicacion
from .forms import PostForm
# Create your views here.
def listar_pub(request):
    pub = Publicacion.objects.filter(fecha_creacion__lte = timezone.now()).order_by('fecha_creacion')
    return render(request, 'blog/listar_pub.html', {'pub':pub})

def detalle_publicar(request, pk):
    pub = get_object_or_404(Publicacion, pk=pk)
    return render(request, 'blog/detalle_publicacion.html', {'pub': pub})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            return redirect('postear', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    pub = get_object_or_404(Publicacion, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=pub)
        if form.is_valid():
            pub = form.save(commit=False)
            pub.author = request.user
            pub.save()
            return redirect('postear', pk=pub.pk)
    else:
        form = PostForm(instance=pub)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    pub = Publicacion.objects.filter(fecha_publicacion__isnull=True).order_by('fecha_creacion')
    return render(request, 'blog/post_draft_list.html', {'pub': pub})

def post_publish(request, pk):
    pub = get_object_or_404(Publicacion, pk=pk)
    pub.publish()
    return redirect('postear', pk=pk)

def post_remove(request, pk):
    pub = get_object_or_404(Publicacion, pk=pk)
    pub.delete()
    return redirect('post_list')



