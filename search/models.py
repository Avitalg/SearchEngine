from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from django.core.exceptions import ObjectDoesNotExist
import re
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage


class Article(models.Model):
    title = models.CharField(max_length=100, default="", blank=False)
    summary = models.CharField(max_length=300, default="", blank=True)
    url = models.URLField(max_length=1000, default="", blank=False, unique=True)
    hide = models.BooleanField(default=False)

    def __str__(self):
        return "id:" + str(self.pk) + ", title:" + str(self.title)

    def get_title(self):
        return str(self.title)

    def get_summary(self):
        return str(self.summary)

    def get_url(self):
        return str(self.url)


class Word(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    data = models.CharField(max_length=20)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return "word:" + str(self.data) + ", article:" + str(self.article.pk) + ", amount:" + str(self.amount)


class Stoplist(models.Model):
    data = models.CharField(max_length=20)

    def __str__(self):
        return str(self.data)


#=================

# @receiver(pre_delete, sender=Article)
# def article_delete(sender, instance, **kwargs):
#     # Pass false so FileField doesn't save the model.
    # instance.file.delete(False)


# @receiver(post_save, sender=Article)
# def article_save(sender, instance, **kwargs):
    # if kwargs['created']:
    #     wordList = re.findall(b"[\w']+", instance.data)
    #     wordList = [word.lower() for word in wordList]
    #     wordList.sort()
    #
    #     for word in wordList:
    #         try:
    #             exist_word = Word.objects.get(data=word, article=instance)
    #             exist_word.amount += 1
    #             exist_word.save()
    #         except (ObjectDoesNotExist, Word.DoesNotExist):
    #             new_word = Word()
    #             new_word.article = instance
    #             new_word.data = word
    #             new_word.amount = 1
    #             new_word.save()

    # else:
    #     Word.objects.filter(article=instance).delete()


