from django.urls import path

from forum_project.main_app import views
from forum_project.main_app.views import CreateArticle

urlpatterns = [
    path('', views.home, name='home'),
    path('profile-details/<int:pk>/', views.ProfileDetails.as_view(), name='profile-details'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('create-post-article/', CreateArticle.as_view(), name='create_post_article'),
    path('create-comment/<int:pk>/', views.CreateComment.as_view(), name='create-comment'),
    path('article-details/<int:pk>/', views.ArticleDetails.as_view(), name='article-details'),
    path('likes/<int:pk>/', views.likes, name='likes'),
    path('like_comment/<int:pk>/', views.like_comment, name='like_comment')
]