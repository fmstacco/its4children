from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.views.generic import View, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Post
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


def index(request):
    """
    Renders the index page
    """
    return render(request, 'index.html')


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "post_list.html"
    paginate_by = 6


class PostDetail(LoginRequiredMixin, View):
    """
    Displays detail post
    """

    def get(self, request, slug, *args, **kwargs):
        """
        Gets detailed post
        """
        queryset = Post.objects
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by("created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )
    
    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by("created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class AddPostView(LoginRequiredMixin, CreateView):
    """
    Logged in user can add a post
    """
    model = Post
    template_name = 'add_post.html'
    fields = ['title', 'content', 'featured_image']

    def form_valid(self, form):
        """
        sets logged in user as author in form
        """
        form.instance.author = self.request.user
        messages.success(
            self.request, 'You have successfully created a activity idea')
        return super(AddPostView, self).form_valid(form)


class UpdatePost(UpdateView):
    model = Post
    fields = ['title', 'content', 'featured_image']
    template_name = 'update_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(UpdatePost, self).form_valid(form)