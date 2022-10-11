from django.urls import path

from forum_project.main_app import views
from forum_project.registration.views import signup

urlpatterns = [
    path('signup/', signup, name='signup')
]