# -*- encoding: utf-8 -*-
'''
a blog model
'''
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.db.models import Count

class CommentsCountManager(models.Manager):
    def get_query_set(self):
        return super(CommentsCountManager, self).get_query_set().annotate(
            votes = Count("vote")).order_by("-votes")

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add = True)
    body = models.TextField()
    tags = TaggableManager()
    author = models.ForeignKey(User)
    def __unicode__(self):
        return self.title
    def excerpt(self):
        return self.body[:300] + u'…'
    class Meta:
        ordering = [u'-created']

class Commentary(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    tags = TaggableManager()
    author = models.ForeignKey(User)
    post = models.ForeignKey(BlogPost)
    score = models.IntegerField(default=0)
    with_votes = CommentsCountManager()
    objects = models.Manager()
    class Meta:
        verbose_name_plural = u'commentaries'
        ordering = [u'-created']
class Vote(models.Model):
    voter = models.ForeignKey(User)
    commentary = models.ForeignKey(Commentary)
    def __unicode__(self):
        return "%s voted %s"(self.voter.username, self.commentary.title)
