from django.shortcuts import render, get_object_or_404
from .models import Article, Word, Stoplist
import json
import re
from collections import Counter
from django.core.files.base import File as DjangoFile

def index(request):
    return render(request, 'search/index.html')


def articles(request):
    all_articles = Article.objects.all()
    context = {
        'all_articles': all_articles,
    }
    return render(request, 'search/articles.html', context)

def details(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'search/detail.html', {'article': article})

def results(request):
    data = request.POST.get('find', "")
    smeth = request.POST.get('smeth', "or")
    exclude_words = Stoplist.objects.values_list("data", flat=True)
    wordlist = re.findall(r"[\w']+", data)
    jsonword = list(set(wordlist)-set(exclude_words))
    articles = articles_id = []
    data = dict()

    if smeth == 'or':
        words = Word.objects.filter(data__in=wordlist).exclude(data__in=exclude_words).order_by('-amount').values("article").distinct()
        articles = Article.objects.filter(id__in=words)

    if smeth == "and":
        words = Word.objects.filter(data__in=wordlist).exclude(data__in=exclude_words).order_by('-amount').values_list('article', flat=True)
        counts = Counter(words)
        for word in words:
            if counts[word] == (len(set(wordlist) - set(exclude_words))):
                articles_id.append(word)

        articles_id = set(articles_id)
        articles = Article.objects.filter(id__in=articles_id)

    if smeth == "not":
        words = Word.objects.filter(data__in=jsonword).order_by('-amount').values("article").distinct()
        articles = Article.objects.exclude(id__in=words)

    for article in articles:
        title = article.file.readline()
        author = article.file.readline()
        text = article.file.read(300)
        data[title] = {"id": article.id, "data": text, "author": author}

    return render(request, 'search/results.html', {'results': articles, 'keywords': jsonword})
#===================================================================================================

def manage(request):
    return render(request, 'manage/index.html')

def addFiles(request):
    return render(request, 'manage/addFiles.html')

def addFilesSubmit(request):
    files = request.FILES.getlist('files')

    for file in files:
        new_file = Article(file=file, hide=False)
        new_file.save()

    return render(request, 'manage/submit.html', {'result': 'result!!!'})