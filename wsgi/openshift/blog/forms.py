# -*- encoding: utf-8 -*-

from django import forms
from blog.models import Commentary

class AddCommentaryForm(forms.ModelForm):
  class Meta:
    model = Commentary
    fields = ('author', 'body')

class SearchForm(forms.Form):
    query = forms.CharField(min_length=3, required=False)
