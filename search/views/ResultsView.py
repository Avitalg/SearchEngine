from django.shortcuts import render
from ..models import Article, Word, Stoplist
import re
from collections import Counter
from django.views import generic
from soundex import getInstance


class ResultsView(generic.ListView):
    template_name = 'search/results.html'
    context_object_name = 'results'
    searches = []

    def post(self, request):
        data = str(request.POST.get('find', ''))
        smeth = request.POST.get('smeth', "or")
        sound = request.POST.get('sound', 'no')
        sound = False if sound == 'no' else True
        ResultsView.searches.insert(0, data)
        data = data.lower()
        exclude_words = Stoplist.objects.values_list("data", flat=True)
        wordlist = re.findall(r"\"*[\w']+\"*", data)
        jsonword = list(set(wordlist)-set(exclude_words))
        if smeth == 'or':
            articles = ResultsView.or_statement(wordlist, False, sound)

        if smeth == "and":
            articles = ResultsView.and_statement(wordlist, False, sound)

        if smeth == "not":
            articles = ResultsView.not_statement(wordlist, "or", sound)

        if smeth == "easy-and":
            articles = ResultsView.easy_and_statement(wordlist, False, sound)

        jsonword = ([s.strip('"') for s in jsonword])

        return render(request, self.template_name, {'results': articles, 'keywords': jsonword,
                                                    "searcher": ResultsView.searches,
                                                    "search": data})

    def or_statement(wordlist, not_stat=False, sound=False):
        wordlist = [word for word in wordlist if word]
        exclude_words = list()
        print("not stat", not_stat)
        print(wordlist)
        if not not_stat:
            exclude_words = ResultsView.excluded_words(wordlist)
        wordlist = ([str(s).strip('"') for s in wordlist])
        contain = [word[:len(word)-1] for word in wordlist if word[len(word)-1] == "*"]
        words_contain = list()

        if sound:
            wordlist = [getInstance().soundex(word) for word in wordlist if word]
            words = Word.objects.filter(soundex__in=wordlist).exclude(data__in=exclude_words).order_by('-amount'). \
                values_list('article', flat=True)
        else:
            if len(contain) > 0:
                for content in contain:
                    words_contain += Word.objects.filter(data__contains=content).exclude(data__in=exclude_words). \
                        values_list('article', flat=True)
                    print("try")
                print("&:", words_contain)
            words = Word.objects.filter(data__in=wordlist).exclude(data__in=exclude_words).order_by('-amount'). \
                values_list('article', flat=True)

        words = list(words) + list(words_contain)
        articles = Article.objects.filter(id__in=words).exclude(hide=True)
        return articles

    def easy_and_statement(wordlist, not_stat=False, sound=False):
        wordlist = [word for word in wordlist if word]
        articles_id = []
        exclude_words = list()
        if not not_stat:
            exclude_words = ResultsView.excluded_words(wordlist)

        wordlist = ([s.strip('"') for s in wordlist])

        if sound:
            wordlist = [getInstance().soundex(word) for word in wordlist if word]
            words = Word.objects.filter(soundex__in=wordlist).exclude(data__in=exclude_words).order_by('-amount').\
            values_list('article', flat=True)
        else:
            words = Word.objects.filter(data__in=wordlist).exclude(data__in=exclude_words).order_by('-amount').\
                values_list('article', flat=True)

        counts = Counter(words)
        for word in words:
            if counts[word] > 0.6*(len(set(wordlist) - set(exclude_words))):
                articles_id.append(word)

        articles_id = set(articles_id)
        return Article.objects.filter(id__in=articles_id).exclude(hide=True)

    def and_statement(wordlist, not_stat=False, sound=False):
        wordlist = [word for word in wordlist if word]
        articles_id = []
        exclude_words = list()
        if not not_stat:
            exclude_words = ResultsView.excluded_words(wordlist)

        wordlist = ([s.strip('"') for s in wordlist])
        exclude_words = list(set(exclude_words) - set(wordlist))

        if sound:
            wordlist = [getInstance().soundex(word) for word in wordlist if word]
            words = Word.objects.filter(soundex__in=wordlist).exclude(data__in=exclude_words).order_by('-amount').\
                values_list('article', flat=True)
        else:
            words = Word.objects.filter(data__in=wordlist).exclude(data__in=exclude_words).order_by('-amount').\
                values_list('article', flat=True)

        counts = Counter(words)

        for word in words:
            if counts[word] == (len(set(wordlist) - set(exclude_words))):
                articles_id.append(word)
        articles_id = set(articles_id)
        return Article.objects.filter(id__in=articles_id).exclude(hide=True)
        # return Postingfile.objects.filter(data__in=wordlist).exclude(data__in=exclude_words)

    def not_statement(wordlist, operand="or", sound=False):
        articles = list()
        exclude_words = ResultsView.excluded_words(wordlist)
        wordlist = ([s.strip('"') for s in wordlist])

        wordlist = list(set(wordlist)-set(exclude_words))
        if operand == "or":
            articles = ResultsView.or_statement(wordlist, True, sound)
        elif operand == "and":
            articles = ResultsView.and_statement(wordlist, True, sound)
        elif operand == "easy-and":
            articles = ResultsView.easy_and_statement(wordlist, True, sound)
        articles = Article.objects.exclude(id__in=articles)
        return articles

    def excluded_words(wordlist):
        exclude_words = Stoplist.objects.values_list("data", flat=True)
        cancel_stoplist = (['"' + word + '"' for word in exclude_words])
        print("cancel: {0}, words: {1}".format(cancel_stoplist, wordlist))
        exclude_words = set(cancel_stoplist) - set(wordlist)
        # print("www", exclude_words)
        exclude_words = ([word[1:len(word) - 1] for word in exclude_words])
        return exclude_words
