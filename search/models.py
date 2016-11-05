from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from django.core.exceptions import ObjectDoesNotExist
import re
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage

# -*- coding: utf-8 -*-


class Article(models.Model):
    title = models.CharField(max_length=100, default="", blank=False)
    summary = models.CharField(max_length=300, default="", blank=True)
    url = models.URLField(max_length=1000, default="", blank=False)
    hide = models.BooleanField(default=False)

    def __str__(self):
        return "id:" + str(self.pk) + ", title:" + str(self.title)

    def get_title(self):
        return str(self.title)

    def get_summary(self):
        return str(self.summary)

    def get_url(self):
        return str(self.url)

    def get_if_hide(self):
        return self.hide


class Word(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    data = models.CharField(max_length=20)
    amount = models.IntegerField(default=1)
    soundex = models.CharField(max_length=10, default="")

    class Meta:
        ordering = ['-amount', 'article']

    def __str__(self):
        return "word:" + str(self.data) + ", article:" + str(self.article.pk) + ", amount:" + str(self.amount) + \
               ",soundex:" + str(self.soundex)


class Stoplist(models.Model):
    data = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return str(self.data)


class Postingfile(models.Model):
    data = models.CharField(max_length=20, blank=False)
    words = models.ManyToManyField(Word)

    def __str__(self):
        return "data:" + str(self.data) +", words:" + str(self.words.all())

    def get_absolute_url(self):
        return reverse('stoplist-view')

