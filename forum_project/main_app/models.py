from django.contrib.auth.models import User
from django.db import models


def topics_choices():
    topics = Topic.objects.all()
    result_as_list = []
    for topic in topics:
        current_value = (topic.name, topic.name)
        result_as_list.append(current_value)
    result = tuple(result_as_list)
    return result


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30)
    profession = models.CharField(max_length=30)
    profile_img = models.ImageField(upload_to='images/', default='images/add_profile_image.jpg')

    def __str__(self):
        return f'profile for: {self.user}'


class Topic(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class PostArticle(models.Model):
    title = models.CharField(max_length=30, unique=True)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length=30, choices=topics_choices(), default='NO TOPIC')

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}: {self.title}"


class ArticleComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_article = models.ForeignKey(PostArticle, on_delete=models.CASCADE)
    content = models.TextField()



