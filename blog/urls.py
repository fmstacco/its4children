from django.urls import path
from . import views


"""url paths"""
urlpatterns = [
    path('', views.index, name='home'),
    path('post_list/', views.PostList.as_view(), name='post_list'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('update_post/', views.UpdatePost.as_view(), name='update_post'), 
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]