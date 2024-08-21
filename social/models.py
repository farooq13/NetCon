from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
  body = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created_on = models.DateTimeField(default=timezone.now)
  likes = models.ManyToManyField(User, related_name='likes', blank=True)
  dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)

  class Meta:
    ordering = ['-created_on']

  def __str__(self):
    return self.body
  
class Comment(models.Model):
  comment = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  created_on = models.DateTimeField(default=timezone.now)

  class Meta:
    ordering = ['-created_on']

  def __str__(self):
    return self.comment
  
class UserProfile(models.Model):
  user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
  name = models.CharField(max_length=100, null=True, blank=True)
  location = models.CharField(max_length=50, null=True, blank=True)
  bio = models.TextField(max_length=200, null=True, blank=True)
  picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/avatar.svg')
  followers = models.ManyToManyField(User, related_name='followers', blank=True)

  def __str__(self):
    return self.name
  

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()

# class Post(models.Model):
#   body = models.TextField()
#   author = models.ForeignKey(User, on_delete=models.CASCADE)
#   created_on = models.DateTimeField(default=timezone.now)
#   likes = models.ManyToManyField(User, related_name='likes', blank=True)
#   dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)

#   class Meta:
#     ordering = ['-created_on']

#   def __str__(self):
#     return self.body
  
# class Comment(models.Model):
#   comment = models.TextField()
#   author = models.ForeignKey(User, on_delete=models.CASCADE)
#   post = models.ForeignKey(Post, on_delete=models.CASCADE)
#   created_on = models.DateTimeField(default=timezone.now)
#   # comment_likes = models.ManyToManyField(User, related_name='comment-likes', blank=True)
#   # comment_dislikes = models.ManyToManyField(User, related_name='comment-dislikes', blank=True)

#   class Meta:
#     ordering = ['-created_on']

#   def __str__(self):
#     return self.comment

# class UserProfile(models.Model):
#   user = models.OneToOneField(User,primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
#   name = models.CharField(max_length=100, null=True, blank=True)
#   location = models.CharField(max_length=100, null=True, blank=True)
#   bio = models.TextField(max_length=100, null=True, blank=True)
#   birth_date = models.DateField(null=True, blank=True)
#   picture = models.ImageField(upload_to='uploads/profile_pictures', default='upoads/profile_pictures/avatar.svg')
#   followers = models.ManyToManyField(User, related_name='followers', blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#   if created:
#     UserProfile.objects.create(use=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#   instance.profile.save()
