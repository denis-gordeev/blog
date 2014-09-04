'''
a blog model
'''
from django.db import models
from django.contrib import admin
from django import forms
from taggit.managers import TaggableManager

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField()
    body = models.TextField()
    tags = TaggableManager()

    def __unicode__(self):
        return self.title
