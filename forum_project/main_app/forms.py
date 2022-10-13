from django import forms

from forum_project.main_app.models import Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']