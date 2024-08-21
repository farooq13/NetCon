from django.urls import path
from .views import PostList, PostDetail, PostEdit, PostDelete


urlpatterns = [
  path('', PostList.as_view(), name='post-list'),
  path('post/<int:pk>/', PostDetail.as_view(), name='post-detail'),
  path('post/edit/<int:pk>/', PostEdit.as_view(), name='post-edit'),
  path('post/delete/<int:pk>/', PostDelete.as_view(), name='post-delete'),
]