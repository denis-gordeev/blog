'''
a blog model
'''
from django.db import models
from django.contrib import admin
from django import forms

class TagsField(models.Field):
    u'''
    Save a list of strings(tags) in a CharField (or TextField) column.

    In the django model object the column is a list of strings.

    based on
    # -*- coding: iso-8859-1 -*-
    # $Id: StringListField.py 344 2009-05-06 06:57:27Z tguettler $
    # $HeadURL: svn+ssh://svnserver/svn/djangotools/trunk/dbfields/StringListField.py $

    # http://www.djangosnippets.org/snippets/1491/
'''
    __metaclass__=models.SubfieldBase
    SPLIT_CHAR=u';'
    def __init__(self, *args, **kwargs):
        self.internal_type=kwargs.pop('internal_type', 'TextField') # or CharField
        super(TagsField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return []
        return value.split(self.SPLIT_CHAR)

    def get_internal_type(self):
        return self.internal_type

    def get_db_prep_lookup(self, lookup_type, value):
        # SQL WHERE
        raise NotImplementedError()

    def get_db_prep_save(self, value):
        return self.SPLIT_CHAR.join(value)

    def formfield(self, **kwargs):
        assert not kwargs, kwargs
        return forms.MultipleChoiceField(choices=self.choices)

class Header(models.Model):
    title = models.CharField(max_length=200)
    timestamp = models.DateTimeField('date published')
    tags = TagsField()
    body = text = models.TextField()

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp')
admin.site.register(BlogPost, BlogPostAdmin)
