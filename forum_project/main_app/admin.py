from django.contrib import admin

from forum_project.main_app.models import Profile, Topic, PostArticle, ArticleComment

admin.site.register(Profile)
admin.site.register(Topic)
admin.site.register(PostArticle)
admin.site.register(ArticleComment)
