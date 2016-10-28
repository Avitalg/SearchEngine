from django.views.generic import TemplateView
from django.shortcuts import render
from search.models import Article
from .ResultsView import ResultsView
import re


class AdvanceSearch(TemplateView):
    template_name = 'search/advance.html'
    model = Article
    oprt = "or"

    def post(self, request):
        data = str(request.POST.get('find', ""))
        results = list(data)
        articles = []
        push_chars, pop_chars = "<({[", ">)}]"
        and_chars, or_chars, not_chars = "&&", "||", "^"
        index, start, error, start_word, not_place = -1, -1, "", -1, -1
        wordlist = []

        for place in range(len(results)):
            # find <({[
            if results[place] in push_chars:
                if start == -11:
                    find_results, words = self.parse_words(data, start_word, place)
                    for result in find_results:
                        articles.append(result)
                    for word in words:
                        wordlist.append(word)
                # if not before brackets
                if start == -111 and not_place == place-1:
                    self.oprt = "not"
                start = place
                index = push_chars.index(results[place])
            # find >)}]
            elif results[place] in pop_chars:
                if index == pop_chars.index(results[place]):
                    find_results, words = self.parse_words(data, start+1, place)
                    for result in find_results:
                        articles.append(result)

                    for word in words:
                        wordlist.append(word)
                    start = -1
                else:
                    error = "Search not valid. No opening brackets to -" + results[place]
                    break
            # find ^
            elif results[place] == not_chars:
                not_place = place
                start = -111
            # start of word without sign
            elif start == -1:
                start_word = place
                start = -11
        if start == -11:
            find_results, words = self.parse_words(data, start_word, len(results))
            if self.oprt == "or":
                articles = set(list(articles) + list(find_results))
            elif self.oprt == "and" or self.oprt == "easy_and":
                if articles:
                    articles = set(find_results) & set(articles)
                else:
                    articles = find_results
            for word in words:
                wordlist.append(word)
        elif start != -1:
            error = "Search not valid. No closing brackets to -" + results[index]

        # for result in results:
        set(articles)
        excluded_word = ResultsView.excluded_words(wordlist)
        wordlist = ([s.strip("'") for s in wordlist])

        wordlist = list(set(wordlist) - set(excluded_word))

        return render(request, 'search/results.html', {"results": articles, "error": error, "keywords": wordlist,
                                                       "searcher": ResultsView.searches})

    def parse_words(self, data, start, place):
        and_chars, or_chars, not_chars, easy_and_chars = "&&", "||", "^", "&"
        new_data = data[start:place]
        wordlist = re.split("&&|\|\|", new_data)

        if new_data.find(and_chars) > -1:
            self.oprt = "and"
        elif new_data.find(easy_and_chars) > -1:
            self.oprt = "easy_and"
        else:
           self.oprt = "or"

        if self.oprt == "not":
            result = ResultsView.not_statement(wordlist, self.oprt)
        else:
            result = ResultsView.or_statement(wordlist)

        ResultsView.searches.insert(0, new_data)
        #remove empty words
        wordlist = [word for word in wordlist if word]
        return result, wordlist