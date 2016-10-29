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
        my_data = data
        results = list(data)
        articles = []
        push_chars, pop_chars = "<({[", ">)}]"
        and_chars, or_chars, not_chars = "&&", "||", "^"
        index, start, second_start,second_index, error, start_word, not_place = -1, -1, -1, -1, "", -1, -1
        wordlist = []
        ResultsView.searches.insert(0, data)

        for place in range(len(results)):
            # find <({[
            if results[place] in push_chars:
                # start of word without sign
                if start == -11:
                    find_results, words = self.parse_words(my_data, start_word, place)
                    if start_word > 0 and results[start_word-1] == "&":
                        articles = AdvanceSearch.and_articles(articles, find_results)
                    else:
                        articles = AdvanceSearch.or_articles(articles, find_results)
                    for word in words:
                        wordlist.append(word)
                    start = place
                    index = push_chars.index(results[place])
                # if 'not' before brackets
                elif (start == -111 or second_start == -111) and not_place == place-1:
                    self.oprt = "not"
                    if second_start == -111:
                        second_start = place
                        second_index = push_chars.index(results[place])
                    else:
                        start = place
                        index = push_chars.index(results[place])
                elif self.oprt == "not" and start != -1:
                    second_start = place
                    second_index = push_chars.index(results[place])
                elif start != -1:
                    second_start = place
                    second_index = push_chars.index(results[place])
                else:
                    start = place
                    index = push_chars.index(results[place])
            # find >)}]
            elif results[place] in pop_chars:
                if index == pop_chars.index(results[place]):
                    find_results, words = self.parse_words(data, start+1, place)
                    if start > -1 and ((results[start-1] == "&") or self.oprt == "and"):
                        articles = AdvanceSearch.and_articles(articles, find_results)
                    elif start > -1 and (results[start-1] == "|" or self.oprt == "or"):
                        articles = AdvanceSearch.or_articles(articles, find_results)
                    elif start > -1 and (results[start-1] == "^" or self.oprt == "not"):
                        articles = not AdvanceSearch.not_articles(articles, find_results)
                    for word in words:
                        wordlist.append(word)
                    start = -1
                elif second_index == pop_chars.index(results[place]):
                    find_results, words = self.parse_words(data, second_start + 1, place)
                    if results[second_start-1] == "^":
                        self.oprt = "not"
                    if second_start > 0 and results[second_start-1] == "&":
                        articles = AdvanceSearch.and_articles(articles, find_results)
                    elif second_start > 0 and results[second_start-1] == "|":
                        articles = AdvanceSearch.or_articles(articles, find_results)
                    elif second_start > 0 and results[second_start-1] == "^":
                        articles = AdvanceSearch.not_articles(articles, find_results)
                    else:
                        articles = find_results
                    for word in words:
                        wordlist.append(word)
                    second_start = -1
                else:
                    error = "Search not valid. No opening brackets to -" + results[place]
                    break
            # find ^
            elif results[place] == not_chars:
                not_place = place
                if start == -1:
                    start = -111
                else:
                    second_start = -111
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
        wordlist = re.split("&&|\|\||\^|&", new_data)
        wordlist = [word for word in wordlist if word]
        result = list()
        type, type2, not_sign = AdvanceSearch.find_type(new_data)

        check_double_brkts = re.findall(r"(.*?)\[.*\]+", new_data)
        regex = re.compile('[^a-zA-Z]')
        type = str()
        type2 = str()
        if check_double_brkts and check_double_brkts[0] != '':
            words_data = re.findall(r"(.*?)\[.*\]+", new_data)
            type, type2, not_sign2 = AdvanceSearch.find_type(words_data)

            words_data = [regex.sub('', word) for word in words_data if word]

        if (not type or (type and type == "&" and type2 == '&')) and new_data.find(and_chars) > -1:
            # wordlist = new_data.split(and_chars)
            if check_double_brkts and check_double_brkts[0] != '':
                wordlist = words_data

            if self.oprt == "not" and not_sign:
                result = ResultsView.not_statement(wordlist, "and")
            else:
                result = ResultsView.and_statement(wordlist)
            self.oprt = "and"
        elif (not type or type == "&") and new_data.find(easy_and_chars) > -1:
            wordlist = re.split("&&|&|\|\|", new_data)
            if self.oprt == "not" and (not type2 or type2 == "^"):
                result = ResultsView.not_statement(wordlist, "easy_and")
            else:
                result = ResultsView.easy_and_statement(wordlist)
            self.oprt = "easy_and"
        else:
            wordlist = new_data.split(or_chars)
            if self.oprt == "not" or (not type2 or type2 == "^") or data[start-2] == '^':
                result = ResultsView.not_statement(wordlist, "or")
            else:
                result = ResultsView.or_statement(wordlist)
            self.oprt = "or"
        # remove empty words
        return result, wordlist

    def and_articles(articles, find_results):
        if not find_results:
            find_results.add("")
        if articles:
            articles = set(articles) & set(find_results)
        else:
            articles = find_results
        return articles

    def or_articles(articles, find_results):
        if articles:
            articles = set(list(articles) + list(find_results))
        else:
            articles = find_results
        return articles

    def not_articles(articles, find_results):
        if articles:
            articles = set(articles) - set(find_results)
        else:
            articles = find_results
        return articles

    def find_type(words_data):
        x = len(words_data)
        y = len(words_data[x - 1])
        type, type2 = "", ""
        not_sign = False
        if x > 0 and y > 0:
            type = words_data[x - 1][y - 2]
        if x > 0 and y > 1:
            type2 = words_data[x - 1][y - 1]
            if y > 2 and type2 == '^':
                not_sign = True
                type2 = words_data[x - 1][y - 3]

        return type, type2, not_sign
