from django import forms
from django.contrib.auth.models import User
from questapp.models import UserProfile


class ClueSearchForm(forms.Form):
    search_txt = forms.CharField(required=False)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
