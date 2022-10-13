from django.urls import path

from forum_project.main_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]