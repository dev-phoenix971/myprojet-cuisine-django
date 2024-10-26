from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import get_user_model
from  blog.models import Blog, BlogComment, Likes
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import BlogForm, CommentForm

import uuid

User = get_user_model()

class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'blog/blog_list.html'
    queryset = Blog.objects.order_by('-publish_date')

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
        # if self.request.user.is_staff:
            return queryset

        return queryset.filter(published=True)


@method_decorator(login_required, name='dispatch')
class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    form = BlogForm()
    template_name = 'blog/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image')

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(" ","-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('blog:blog_list'))
    


def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    already_liked = Likes.objects.filter(blog=blog, user=request.user.id)
    if already_liked:
        liked = True
    else:
        liked = False

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('blog:blog_details', kwargs={'slug':slug}))
    

    return render(request, 'blog/blog_details.html', context={'blog':blog, 'comment_form':comment_form, 'liked':liked})
    

    

# class DetailBlog(LoginRequiredMixin, DetailView):
#     model = Blog
#     context_object_name = "blog"
#     template_name = 'blog/blog_details.html'



class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    form = BlogForm()
    template_name = 'blog/edit_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image', 'published')



class DeleteBlog(LoginRequiredMixin, DeleteView):
    model = Blog
    context_object_name = "blog"
    success_url = reverse_lazy("blog:blog_list")


@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)

    if not already_liked:
        liked_post = Likes(blog=blog, user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('blog:blog_details', kwargs={'slug':blog.slug}))


@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('blog:blog_details', kwargs={'slug':blog.slug}))