from django.urls import path

from forum_project.main_app import views
from forum_project.registration.views import signup, login_page, logout_page

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
]