from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forum_project.registration.urls')),
    path('', include('forum_project.main_app.urls')),

]
