from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm
from forum_project.main_app.models import Profile


def update_user_data(user):
    Profile.objects.update_or_create(user=user, defaults={
        'profession': user.profession,
        'city': user.city,
    }, )


def signup(request):
    title = 'REGISTRATION'
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.city = form.cleaned_data.get('city')
            user.profession = form.cleaned_data.get('profession')
            update_user_data(user)

            user.save()
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form, 'title': title})


def login_page(request):
    form = LogInForm()
    title = 'LOGIN'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # messages.info(request, 'You successfully login.')
            return redirect('home')
        # else:
        #     messages.error(request, f'User name: "{username}" or password is not correct.')

    return render(request, 'registration.html', context={'form': form, 'title': title}, )


def logout_page(request):
    logout(request)
    return redirect('home')

