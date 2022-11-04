from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from forum_project.main_app.forms import EditProfileForm
from forum_project.main_app.models import Profile, Topic, PostArticle, ArticleComment


def home(request, pk=None):
    topics = Topic.objects.all()
    profiles = Profile.objects.all()
    if pk:
        topic = Topic.objects.get(id=pk)
        articles = PostArticle.objects.filter(topic=topic).order_by('-date_created')
        len_articles = len(PostArticle.objects.filter(topic=topic))
        if len_articles:
            title_for_articles_container = f'{len_articles} posts for topic "{topic}"'
        else:
            title_for_articles_container = f'There are not post for topic "{topic}"'
    else:
        articles = PostArticle.objects.all().order_by('-date_created')
        title_for_articles_container = 'Latest Posts'

    p = Paginator(articles, 4)
    page = request.GET.get('page')
    articles_paginator = p.get_page(page)
    context = {
        'title_for_articles_container': title_for_articles_container,
        'topics': topics,
        'profiles': profiles,
        'articles_paginator': articles_paginator,
    }
    return render(request, 'home.html', context)


class MyArticlesList(LoginRequiredMixin, ListView):
    model = PostArticle
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        current_user = User.objects.get(id=pk)
        if not current_user == self.request.user:
            raise PermissionDenied(" WARNING: You do not have permission to EDIT Article of Other Users, Be Careful!!!")
        return super(MyArticlesList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MyArticlesList, self).get_context_data(*args, **kwargs)
        context['title_for_articles_container'] = 'MY ARTICLES'
        context['topics'] = Topic.objects.all()
        context['profiles'] = Profile.objects.all()
        current_user = User.objects.get(id=self.kwargs['pk'])
        articles = PostArticle.objects.filter(user=current_user)
        p = Paginator(articles, 3)
        page = self.request.GET.get('page')
        context['articles_paginator'] = p.get_page(page)
        return context


def search_article(request):
    articles_list = PostArticle.objects.all()
    query = request.GET.get('q')
    if query:
        articles_list = PostArticle.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(user__username__contains=query)
        ).order_by('-date_created')

    paginator = Paginator(articles_list, 2)  # 6 posts per page
    page = request.GET.get('page')

    try:
        articles_paginator = paginator.page(page)
    except PageNotAnInteger:
        articles_paginator = paginator.page(1)
    except EmptyPage:
        articles_paginator = paginator.page(paginator.num_pages)

    context = {
        'articles_paginator': articles_paginator,
        'topics': Topic.objects.all(),
        'profiles': Profile.objects.all(),
        'title_for_articles_container': f'You search for "{query}"',
    }
    return render(request, "home.html", context)


def edit_profile(request):
    title = 'EDIT PROFILE'
    button_title = 'EDIT'
    user_profile = request.user.profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditProfileForm(instance=user_profile)
    context = {'form': form,
               'title': title,
               'profile': user_profile,
               'button_title': button_title, }
    return render(request, 'registration.html', context)


class CreateArticle(LoginRequiredMixin, CreateView):
    model = PostArticle
    fields = ['title', 'content', 'topic']
    template_name = 'form.html'
    success_url = reverse_lazy('home')
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CreateArticle, self).get_context_data(*args, **kwargs)
        context['title'] = 'CREATE ARTICLE'
        context['button_title'] = 'CREATE'
        return context


class ArticleDetails(DetailView):
    model = PostArticle
    template_name = 'article-detail.html'
    context_object_name = "article"

    def get_context_data(self, *args, **kwargs):
        current_article = PostArticle.objects.get(id=self.kwargs['pk'])
        comments = reversed(current_article.articlecomment_set.all())
        context = super(ArticleDetails, self).get_context_data(*args, **kwargs)

        context['comments'] = comments
        return context


class EditArticle(LoginRequiredMixin, UpdateView):
    model = PostArticle
    template_name = 'form.html'
    fields = ['title', 'content', 'topic', ]

    def get_object(self, *args, **kwargs):
        obj = super(EditArticle, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied(" WARNING: You do not have permission to EDIT Article of Other Users, Be Careful!!!")
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(EditArticle, self).get_context_data(*args, **kwargs)
        context['title'] = 'EDIT ARTICLE'
        context['button_title'] = 'EDIT'
        return context

    def get_success_url(self):
        current_article = PostArticle.objects.get(id=self.kwargs['pk'])
        return reverse('article-details', kwargs={"pk": current_article.id})


class DeleteArticle(LoginRequiredMixin, DeleteView):
    model = PostArticle
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def get_object(self, *args, **kwargs):
        obj = super(DeleteArticle, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied(
                " WARNING: You do not have permission to DELETE Article of Other Users, Be Careful!!!")
        return obj

    def get_context_data(self, *args, **kwargs):
        current_article = PostArticle.objects.get(id=self.kwargs['pk'])
        context = super(DeleteArticle, self).get_context_data(*args, **kwargs)
        context['title'] = f'Do you want to delete {current_article.title}?'
        context['button_title'] = 'DELETE'
        return context


class CreateComment(LoginRequiredMixin, CreateView):
    model = ArticleComment
    fields = ['content', ]
    template_name = 'form.html'

    def form_valid(self, form):
        current_article = PostArticle.objects.get(id=self.kwargs['pk'])
        form.instance.post_article = current_article
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        current_article = PostArticle.objects.get(id=self.kwargs['pk'])
        context = super(CreateComment, self).get_context_data(*args, **kwargs)
        context['title'] = f'comment to article "{current_article.title}"'
        context['button_title'] = 'comment'
        return context

    def get_success_url(self):
        current_article = PostArticle.objects.get(id=self.kwargs['pk'])
        return reverse('article-details', kwargs={"pk": current_article.id})


class EditComment(LoginRequiredMixin, UpdateView):
    model = ArticleComment
    template_name = 'form.html'
    fields = ['content']

    def get_object(self, *args, **kwargs):
        obj = super(EditComment, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied(
                " WARNING: You do not have permission to EDIT Comment from Other Users, Be Careful!!!")
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(EditComment, self).get_context_data(*args, **kwargs)
        context['title'] = 'EDIT COMMENT'
        context['button_title'] = 'EDIT'
        return context

    def get_success_url(self):
        current_comment = ArticleComment.objects.get(id=self.kwargs['pk'])
        current_article = current_comment.post_article
        return reverse('article-details', kwargs={"pk": current_article.id})


class DeleteComment(LoginRequiredMixin, DeleteView):
    model = ArticleComment
    template_name = 'form.html'

    def get_object(self, *args, **kwargs):
        obj = super(DeleteComment, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user and not obj.post_article.user == self.request.user:
            raise PermissionDenied(
                " WARNING: You do not have permission to DELETE Comment from Other Users, Be Careful!!!")
        return obj

    def get_context_data(self, *args, **kwargs):
        current_comment = ArticleComment.objects.get(id=self.kwargs['pk'])
        context = super(DeleteComment, self).get_context_data(*args, **kwargs)
        context['title'] = f'Do you want to delete comment from {current_comment.user.profile.full_name}?'
        context['button_title'] = 'DELETE'
        return context

    def get_success_url(self):
        current_comment = ArticleComment.objects.get(id=self.kwargs['pk'])
        current_article = current_comment.post_article
        return reverse('article-details', kwargs={"pk": current_article.id})


@login_required
def likes(request, pk):
    current_article = PostArticle.objects.get(id=pk)
    if request.user not in current_article.users_which_liked_article.all():
        current_article.users_which_liked_article.add(request.user)
        current_article.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def like_comment(request, pk):
    current_comment = ArticleComment.objects.get(id=pk)
    if request.user not in current_comment.users_which_liked_comment.all():
        current_comment.users_which_liked_comment.add(request.user)
        current_comment.save()
    return redirect('article-details', current_comment.post_article.id)


class ProfileDetails(DetailView):
    model = Profile
    template_name = 'profile-details.html'
    context_object_name = 'profile'
