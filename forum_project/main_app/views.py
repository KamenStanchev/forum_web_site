from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from forum_project.main_app.forms import EditProfileForm, PostArticleForm
from forum_project.main_app.models import Profile, Topic, PostArticle


def home(request):
    topics = Topic.objects.all()
    profiles = Profile.objects.all()
    context={
        'topics': topics,
        'profiles': profiles,
    }
    return render(request, 'home.html', context)


def edit_profile(request):
    title = 'EDIT PROFILE'
    user_profile = request.user.profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditProfileForm(instance=user_profile)
    return render(request, 'registration.html', {'form': form, 'title': title, 'profile': user_profile})


class CreatePostArticle(LoginRequiredMixin, CreateView):
    model = PostArticle
    fields = ['title', 'content', 'topic']
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CreatePostArticle, self).get_context_data(*args, **kwargs)
        context['title'] = 'CREATE ARTICLE'
        return context


