from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Post


class PublishedPostListView(ListView):
    model = Post
    template_name = 'blog/published_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class UnpublishedPostListView(ListView):
    model = Post
    template_name = 'blog/unpublished_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(is_published=False)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views_count += 1
        post.save()
        return post


class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:published_post_list')


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

    def get_success_url(self):
        return reverse_lazy('blog:unpublished_post_list', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:unpublished_post_list')
