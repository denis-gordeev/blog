# -*- encoding: utf-8 -*-
'''
a blog model
'''
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.db.models import Count
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import hashlib

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
        ordering = [u'created']

class Vote(models.Model):
    voter = models.ForeignKey(User)
    commentary = models.ForeignKey(Commentary)
    def __unicode__(self):
        return "%s voted %s"(self.voter.username, self.commentary.title)

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)
    crocies_rep = models.IntegerField(default=0)
    pythons_rep = models.IntegerField(default=0)
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False
    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
