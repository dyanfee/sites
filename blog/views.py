from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category
from comments.form import CommentForm
import markdown
from django.views.generic import ListView
# Create your views here.


class IndexView(ListView):
    model = Post
    template_name = "index.html"
    context_object_name = 'post_list'


def index(request):
    post_list = Post.objects.all()
    return render(request, 'index.html', context={
        "post_list": post_list
    })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 阅读量+1
    post.increase_views()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'detail.html', context=context)


def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month)
    return render(request, 'index.html', context={'post_list': post_list})


class ArchivesView(IndexView):
    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(create_time__month=self.kwargs.get('month'),
                                                               create_time__year=self.kwargs.get('year'))


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'index.html', context={'post_list': post_list})


class CategoryView(IndexView):
    # model = Post
    # template_name = 'index.html'
    # context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
