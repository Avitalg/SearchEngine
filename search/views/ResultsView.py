from django.shortcuts import render
from ..models import Article, Word, Stoplist, Postingfile
import re
from collections import Counter
from django.views import generic


class ResultsView(generic.ListView):
    template_name = 'search/results.html'
    context_object_name = 'results'
    searches = []

    def post(self, request):
        data = str(request.POST.get('find', ""))
        ResultsView.searches.insert(0, data)
        smeth = request.POST.get('smeth', "or")
        exclude_words = Stoplist.objects.values_list("data", flat=True)
        wordlist = re.findall(r"[\w']+", data)
        wordlist = set(wordlist)
        jsonword = list(set(wordlist)-set(exclude_words))
        if smeth == 'or':
            articles = ResultsView.or_statement(wordlist)

        if smeth == "and":
            articles = ResultsView.and_statement(wordlist)

        if smeth == "not":
            words = Word.objects.filter(data__in=jsonword).values("article")
            articles = Article.objects.exclude(id__in=words).exclude(hide=True)

        if smeth == "easy-and":
            articles = ResultsView.easy_and_statement(wordlist)

        jsonword = ([s.strip("'") for s in jsonword])

        return render(request, self.template_name, {'results': articles, 'keywords': jsonword, "searcher": ResultsView.searches})

    def or_statement(wordlist, not_stat=False):
        wordlist = [word for word in wordlist if word]
        exclude_words = list()
        print('or')
        if not not_stat:
            exclude_words = ResultsView.excluded_words(wordlist)
        wordlist = ([str(s).strip("'") for s in wordlist])
        words = Word.objects.filter(data__in=wordlist).exclude(data__in=exclude_words).order_by('-amount').\
            values("article")
        return Article.objects.filter(id__in=words).exclude(hide=True)

    def easy_and_statement(wordlist, not_stat=False):
        wordlist = [word for word in wordlist if word]
        print("easy and", wordlist)
        articles_id = []
        exclude_words = list()
        if not not_stat:
            exclude_words = ResultsView.excluded_words(wordlist)

        wordlist = ([s.strip("'") for s in wordlist])

        exclude_words = list(set(exclude_words) - set(wordlist))
        words = Word.objects.filter(data__in=wordlist).exclude(data__in=exclude_words).order_by('-amount').\
            values_list('article', flat=True)

        counts = Counter(words)
        for word in words:
            if counts[word] > 0.6*(len(set(wordlist) - set(exclude_words))):
                articles_id.append(word)

        articles_id = set(articles_id)
        return Article.objects.filter(id__in=articles_id).exclude(hide=True)

    def and_statement(wordlist, not_stat=False):
        wordlist = [word for word in wordlist if word]
        articles_id = []
        exclude_words = list()
        if not not_stat:
            exclude_words = ResultsView.excluded_words(wordlist)

        wordlist = ([s.strip("'") for s in wordlist])
        exclude_words = list(set(exclude_words) - set(wordlist))
        print("ex:", exclude_words)
        print("sec:", wordlist)
        # print("test:")
        # print(wordlist)
        # print(exclude_words)
        words = Word.objects.filter(data__in=wordlist).exclude(data__in=exclude_words).order_by('-amount').\
            values_list('article', flat=True)

        counts = Counter(words)

        for word in words:
            if counts[word] == (len(set(wordlist) - set(exclude_words))):
                articles_id.append(word)
        articles_id = set(articles_id)
        print(articles_id)
        return Article.objects.filter(id__in=articles_id).exclude(hide=True)
        # return Postingfile.objects.filter(data__in=wordlist).exclude(data__in=exclude_words)

    def not_statement(wordlist, operand="or"):
        print("okkkkk")
        articles = list()
        exclude_words = ResultsView.excluded_words(wordlist)
        wordlist = ([s.strip("'") for s in wordlist])
        wordlist = list(set(wordlist)-set(exclude_words))
        if operand == "or":
            articles = ResultsView.or_statement(wordlist, True)
        elif operand == "and":
            articles = ResultsView.and_statement(wordlist, True)
        elif operand == "easy-and":
            articles = ResultsView.easy_and_statement(wordlist, True)

        return Article.objects.exclude(id__in=articles)

    def excluded_words(wordlist):
        exclude_words = Stoplist.objects.values_list("data", flat=True)
        cancel_stoplist = (["'" + word + "'" for word in exclude_words])
        # print(cancel_stoplist)
        # print(wordlist)
        exclude_words = set(cancel_stoplist) - set(wordlist)
        exclude_words = ([word[1:len(word) - 1] for word in exclude_words])
        return exclude_words
