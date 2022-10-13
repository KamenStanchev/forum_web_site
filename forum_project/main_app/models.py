from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30)
    profession = models.CharField(max_length=30)
    profile_img = models.ImageField(upload_to='images/', default='images/add_profile_image.jpg')
