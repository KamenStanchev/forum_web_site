from django.urls import path

from forum_project.main_app import views
from forum_project.main_app.views import CreatePostArticle

urlpatterns = [
    path('', views.home, name='home'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('create-post-article/', CreatePostArticle.as_view(), name='create_post_article')
]