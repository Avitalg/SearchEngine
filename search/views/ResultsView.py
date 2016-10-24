from django.shortcuts import render
from ..models import Article, Word, Stoplist, Postingfile
import re
from collections import Counter
from django.views import generic
from django.db.models import Case, When


class ResultsView(generic.ListView):
    template_name = 'search/results.html'
    context_object_name = 'results'

    def post(self, request, *args, **kwargs):
        data = request.POST.get('find', "")
        smeth = request.POST.get('smeth', "or")
        exclude_words = Stoplist.objects.values_list("data", flat=True)
        wordlist = re.findall(r"[\w']+", data)
        wordlist = set(wordlist)
        jsonword = list(set(wordlist)-set(exclude_words))
        if smeth == 'or':
            words = Postingfile.objects.filter(data__in=wordlist).exclude(data__in=exclude_words)

            for word in words:
                words[word] = set(word)


        if smeth == "and":
            words = Postingfile.objects.filter(data__in=wordlist).exclude(data__in=exclude_words)
            # counts = Counter(words)
            # for word in words:
            #     if counts[word] == (len(set(wordlist) - set(exclude_words))):
            #         articles_id.append(word)
            #
            # articles_id = set(articles_id)
            # articles = Article.objects.filter(id__in=articles_id).exclude(hide=True)

        if smeth == "not":
            words = Word.objects.filter(data__in=jsonword).values("article")
            articles = Article.objects.exclude(id__in=words).exclude(hide=True)

        return render(request, self.template_name, {'results': words, 'keywords': jsonword})

