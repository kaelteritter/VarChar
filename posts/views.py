from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CommentForm

from .models import Post


def home(request):
    posts = Post.objects.all()
    form = CommentForm()
    context = {
        'posts': posts,
        'form': form
    }
    return render(request, 'index.html', context=context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})


def create_comment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_post = Post.objects.get(pk=post_id)
            comment.author = request.user
            comment.save()
        else:
            print(form.errors)
        return redirect('posts:home')
    else:
        return redirect('posts:home')