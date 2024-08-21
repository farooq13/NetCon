from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Q
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm

  

class PostList(View):
  def get(self, request, *args, **kwargs):
    posts = Post.objects.filter(
      Q(author__profile__followers__in=[request.user.id]) |
      Q(author=request.user)
    )
    form = PostForm()

    context = {'posts': posts, 'form': form}
    return render(request, 'social/post_list.html', context)
  
  def post(self, request, *args, **kwargs):
    posts = Post.objects.filter(
      Q(author__profile__followers__in=[request.user.id]) |
      Q(author=request.user)
    )
    form = PostForm(request.POST)

    if form.is_valid():
      new_post = form.save(commit=False)
      new_post.author = request.user
      new_post.save()
    
    context = {'posts': posts, 'form': form}
    return render(request, 'social/post_list.html', context)
  
class PostDetail(LoginRequiredMixin, View):
  def get(self, request, pk, *args, **kwargs):
    post = Post.objects.get(pk=pk)
    form = CommentForm()

    context = {'post': post, 'form': form}
    return render(request, 'social/post_detail.html', context)
  
  def post(self, request, pk, *args, **kwargs):
    post = Post.objects.get(pk=pk)
    form = CommentForm(request.POST)

    if form.is_valid():
      new_comment = form.save(commit=False)
      new_comment.post = post
      new_comment.author = request.user
      new_comment.save()

    context = {'post': post, 'form': form}
    return render(request, 'social/post_detail.html', context)
  
class PostEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  fields = ['body']
  template_name = 'social/post_edit.html'

  def get_success_url(self):
    pk = self.kwargs['pk']
    return reverse_lazy('post-detail', kwargs={'pk':pk})
  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
  
class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  template_name = 'social/post_delete.html'
  success_url = reverse_lazy('post-list')
  
  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author

# class PostList(View):
#   def get(self, request, *args, **kwargs):
#     posts = Post.objects.filter(
#       Q(author__profile__followers__in=[request.user.id]) |
#       Q(author=request.user)
#     )
#     form = PostForm()
    
#     context = {'posts': posts, 'form': form}
#     return render(request, 'social/post_list.html', context)
  
#   def post(self, request, *args, **kwargs):
#     posts = Post.objects.all()
#     form = PostForm(request.POST)
    
#     if form.is_valid():
#       new_post = form.save(commit=False)
#       new_post.autor = request.user
#       new_post.save()

#     context = {'posts': posts, 'form': form}
#     return render(request, 'social/post_list.html', context)
  
# class PostDetail(LoginRequiredMixin, View):
#   def get(self, request, pk, *args, **kwargs):
#     post = Post.objects.get(pk=pk)
#     form = CommentForm()
#     comments = Comment.objects.all()

#     context = {'post': post, 'form': form, 'comments': comments}
#     return render(request, 'social/post_detail.html', context)
  
#   def post(self, request, pk, *args, **kwargs):
#     post = Post.objects.get(pk=pk)
#     form = CommentForm(request.POST)
#     comments = Comment.objects.all()

#     if form.is_valid():
#       new_comment = form.save(commit=False)
#       new_comment.author = request.user
#       new_comment.post = post
#       new_comment.save()

#     context = {'post': post, 'form': form, 'comments': comments}
#     return render(request, 'social/post_detail.html', context)
  
# class PostEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#   model = Post
#   fields = ['body']
#   template_name = 'social/post_edit.html'

#   def get_success_url(self):
#     pk = self.kwargs['pk']
#     return reverse_lazy('post-detail', kwargs={'pk': pk})
  
#   def test_func(self):
#     post = self.get_object()
#     return self.request.user == post.author

# class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#   model = Post
#   template_name = 'social/post_delete.html'
#   success_url = reverse_lazy('post-list')

#   def test_func(self):
#     post = self.get_object()
#     return self.request.user == post.author
  
# class PostLike(LoginRequiredMixin, View):
#   def post(self, request, pk, *args, **kwargs):
#     post = Post.objects.get(pk=pk)
    
#     is_dislike = False
#     for dislike in post.dislikes.all():
#       if dislike == request.user:
#         post.dislikes.remove(request.user)
#         break
#     is_like = False
#     for like in post.likes.all():
#       if like == request.user:
#         is_like = True
#         break
#     if not is_like:
#       post.likes.add(request.user)
#     if is_like:
#       post.likes.remove(request.user)

#     next = request.POST.get('next')
#     return HttpResponseRedirect(next, '/')

# class PostDislike(LoginRequiredMixin, View):
#   def post(self, request, pk, *args, **kwargs):
#     post = Post.objects.get(pk=pk)

#     is_like = False
#     for like in post.likes.all():
#       if like == request.user:
#         post.likes.remove(request.user)
#         break
#     is_dislike = False
#     for dislike in post.dislikes.all():
#       if dislike == request.user:
#         is_dislike = True
#         break
#     if not is_dislike:
#       post.dislikes.add(request.user)
#     if is_dislike:
#       post.dislikes.remove(request.user)

#     next = request.POST.get('next')
#     return HttpResponseRedirect(next, '/')

# class CommentEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#   model = Comment
#   fields = ['comment']
#   template_name = 'social/comment_edit.html'

#   def get_success_url(self):
#     pk = self.kwargs['pk']
#     return reverse_lazy('post-detail', kwargs={'pk': pk})
  
#   def test_func(self):
#     comment = self.get_object()
#     return self.request.user == comment.author
  
# class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#   model = Comment
#   template_name = 'social/comment_delete.html'
  
#   def get_success_url(self):
#     pk = self.kwargs['pk']
#     return reverse_lazy('post-detail', kwargs={'pk': pk})

#   def test_func(self):
#     comment = self.get_object()
#     return self.request.user == comment.author
  
# class Profile(View):
#   def get(self, request, pk, *args, **kwargs):
#     profile = UserProfile.objects.get(pk=pk)
#     user = profile.user
#     followers = profile.followers.all()
#     number_of_followers = len(followers)
#     is_following = False

#     for follower in followers:
#       if follower == request.user:
#         is_following = True
#       else:
#         is_following = False

#     context = {'profile': profile, 'user': user, 'followers': followers, 'is_following': is_following, 'number_of_followers': number_of_followers}
#     return render(request, 'social/profile.html', context)
  
# class ProfileEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#   model = UserProfile
#   fields = ['picture', 'name', 'location', 'bio', 'birth_date']
#   template_name = 'social/profile_edit.html'

#   def get_success_url(self):
#     pk = self.kwargs['pk']
#     return reverse_lazy('user-profile', kwargs={'pk': pk})
  
#   def test_func(self):
#     profile = self.get_object()
#     return self.request.user == profile.user

# class AddFollower(LoginRequiredMixin, View):
#   def post(self, request, pk, *args, **kwargs):
#     profile = UserProfile.objects.get(pk=pk)
#     profile.followers.add(request.user)
#     return redirect('user-profile', pk=profile.pk)

# class RemoveFollower(LoginRequiredMixin, View):
#   def post(self, request, pk, *args, **kwargs):
#     profile = UserProfile.objects.get(pk=pk)
#     profile.followers.remove(request.user)
#     return redirect('user-profile', pk=profile.pk)
  
# class UserSearch(View):
#   def get(self, request, *args, **kwargs):
#     query = request.GET.get('query')
#     profile_list = UserProfile.objects.filter(
#       Q(user__username__icontains=query)
#     )

#     context = {'profile_list': profile_list}
#     return render(request, 'social/search.html', context)
  
# class ListFollowers(View):
#   def get(self, request, pk, *args, **kwargs):
#     profile = UserProfile.objects.get(pk=pk)
#     followers = profile.followers.all()

#     context = {'profile': profile, 'followers': followers}
#     return render(request, 'social/followers_list.html', context)