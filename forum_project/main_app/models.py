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


def calculate_likes(list_of_objects):
    likes = 0
    for obj in list_of_objects:
        likes += obj.likes
    return likes


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30)
    profession = models.CharField(max_length=30)
    profile_img = models.ImageField(upload_to='images/', default='images/add_profile_image.jpg')

    def __str__(self):
        return f'profile for: {self.user}'

    @property
    def received_likes(self):
        post_articles = self.user.postarticle_set.all()
        post_comments = self.user.articlecomment_set.all()
        result = calculate_likes(post_articles) + calculate_likes(post_comments)
        return result

    @property
    def all_post_articles(self):
        post_articles = self.user.postarticle_set.all()
        result = len(post_articles)
        return result

    @property
    def all_comments(self):
        post_comments = self.user.articlecomment_set.all()
        result = len(post_comments)
        return result


class Topic(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class PostArticle(models.Model):
    title = models.CharField(max_length=30, unique=True)
    content = models.TextField()
    # likes = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length=30, choices=topics_choices(), default='NO TOPIC')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    users_which_liked_article = models.ManyToManyField(
        User,
        related_name='user_lied_article',
        blank=True,
    )

    @property
    def likes(self):
        result = len(self.users_which_liked_article.all())
        return result

    def __str__(self):
        return f"{self.user}: {self.title}"

    @property
    def comments(self):
        result = self.articlecomment_set.all()
        return result


class ArticleComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_article = models.ForeignKey(PostArticle, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    data_created = models.DateTimeField(auto_now_add=True)
    # likes = models.IntegerField(default=0)
    users_which_liked_comment = models.ManyToManyField(
        User,
        related_name='user_lied_comment',
        blank=True,
    )

    @property
    def likes(self):
        result = len(self.users_which_liked_comment.all())
        return result





