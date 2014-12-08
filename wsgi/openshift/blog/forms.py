# -*- encoding: utf-8 -*-

from django import forms
from blog.models import Commentary, UserProfile
from django.contrib.auth.models import User

class AddCommentaryForm(forms.ModelForm):
    class Meta:
        #form.base_fields['author'].initial = request.user
        model = Commentary
        author = forms.CharField()
        body = forms.CharField(widget=forms.Textarea)
        fields = ('body',)

class SearchForm(forms.Form):
    query = forms.CharField(min_length=3, required=False)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
