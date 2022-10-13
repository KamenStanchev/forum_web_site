from django.shortcuts import render, redirect

from forum_project.main_app.forms import EditProfileForm
from forum_project.main_app.models import Profile


def home(request):
    return render(request, 'home.html')


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
