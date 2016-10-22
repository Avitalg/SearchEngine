from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from django.core.exceptions import ObjectDoesNotExist
import re
from django.core.urlresolvers import reverse


class Article(models.Model):
    file = models.FileField(null=True, blank=True)
    hide = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('search:details', kwargs={'pk': self.pk})

    def __str__(self):
        return "id:" + str(self.pk) + "\ttitle:" + str(self.get_title())

    def get_id(self):
        return self.id

    def get_title(self):
        self.file.open()
        text = self.file.readline()
        self.file.close()
        return text

    def get_author(self):
        self.file.open()
        self.file.readline()
        text = self.file.readline()
        self.file.close()
        return text

    def get_summary(self):
        self.file.open()
        self.file.readline()
        self.file.readline()
        text = self.file.read(300)
        self.file.close()
        return text

    def get_data(self):
        self.file.open()
        self.file.readline()
        self.file.readline()
        text = self.file.read()
        self.file.close()
        return text

    # def save(self):


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

@receiver(pre_delete, sender=Article)
def article_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)


@receiver(post_save, sender=Article)
def article_save(sender, instance, **kwargs):
    if kwargs['created']:
        data = instance.file.read()
        wordList = re.findall(b"[\w']+", data)
        wordList = [word.lower() for word in wordList]
        wordList.sort()

        for word in wordList:
            try:
                exist_word = Word.objects.get(data=word, article=instance)
                exist_word.amount += 1
                exist_word.save()
            except (ObjectDoesNotExist, Word.DoesNotExist):
                new_word = Word()
                new_word.article = instance
                new_word.data = word
                new_word.amount = 1
                new_word.save()

    else:
        Word.objects.filter(article=instance).delete()


