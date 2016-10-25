from django.views.generic import TemplateView
from django.shortcuts import render
from search.models import Article
from .ResultsView import ResultsView
import re

class AdvanceSearch(TemplateView):
    template_name = 'search/advance.html'
    model = Article
    searches = []
    test = []
    oprt = "or"

    def post(self, request, *args, **kwargs):
        data = request.POST.get('find', "")
        results = list(data)
        articles = []
        pushChars, popChars = "<({[", ">)}]"
        andChars, orChars, notChars = "&&", "||", "^"
        index, start, error, start_word = -1, -1, "", -1
        wordlist = []

        for place in range(len(results)):
            if results[place] in pushChars:
                if start == -11:
                    find_results, words = self.parse_words(data, start_word, place)
                    for result in find_results:
                        articles.append(result)
                    for word in words:
                        wordlist.append(word)
                if start == -111:
                    self.oprt = "not"
                start = pushChars.index(results[place])
                index = place
            elif results[place] in popChars:
                if start == popChars.index(results[place]):
                    find_results, words = self.parse_words(data, start+1 , place)
                    for result in find_results:
                        articles.append(result)

                    for word in words:
                        wordlist.append(word)
                    start = -1
                else:
                    error = "Search not valid. No opening brackets to -" + results[place]
                    break
            elif results[place] == notChars:
                start = -111

            elif start == -1:
                start_word = place
                start = -11
        if start == -11:
            find_results, words = self.parse_words(data, start_word, len(results))
            if self.oprt == "or":
                articles = set(list(articles) + list(find_results))
            elif self.oprt == "and":
                articles = set(find_results) & set(articles)
            for word in words:
                wordlist.append(word)
        elif start != -1:
            error = "Search not valid. No closing brackets to -" + results[index]

        # for result in results:
        set(articles)
        return render(request, 'search/results.html', {"results": articles, "error": error, "keywords": wordlist,
                                                       "searcher": self.searches})

    def parse_words(self, data, start, place):
        andChars, orChars, notChars = "&&", "||", "^"
        new_data = data[start:place]
        if new_data.find(andChars) > -1:
            wordlist = new_data.split(andChars)
            if( self.oprt == "not"):
                result = ResultsView.not_statement(wordlist, "and")
            else:
                result = ResultsView.and_statement(wordlist)
            self.oprt = "and"
        else:
            wordlist = new_data.split(orChars)
            if(self.oprt == "not"):
                result = ResultsView.not_statement(wordlist, "or")
            else:
                result = ResultsView.or_statement(wordlist)
            self.test.append(wordlist)
            self.oprt = "or"

        self.searches.append(new_data)
        wordlist = [word for word in wordlist if word]
        return result, wordlist