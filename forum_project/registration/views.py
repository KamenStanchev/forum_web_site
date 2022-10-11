from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import SignUpForm
from .models import Profile


def update_user_data(user):
    Profile.objects.update_or_create(user=user, defaults={
        'profession': user.profession,
        'city': user.city,
    }, )


def signup(request):
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
    return render(request, 'signup.html', {'form': form})