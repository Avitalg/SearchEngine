from django.views.generic import TemplateView
from search.models import Article
from .ResultsView import ResultsView
import re
from django.shortcuts import render


class AdvanceSearch(TemplateView):
    template_name = 'search/advance.html'
    model = Article
    first_not_flag, second_not_flag = False, False

    def post(self, request):
        data = str(request.POST.get('find', ""))
        first_start, second_start, second_end = -1, -1, -1
        results = []
        wordlist = []
        error = ""
        first_result_flag = True
        ResultsView.searches.insert(0, data)
        data = data.lower()

        for place in range(len(data)):
            if data[place] == "^" and first_start == -1:
                self.first_not_flag = True
            elif data[place] == "^" and second_start == -1:
                self.second_not_flag = True
            elif data[place] == "(":
                first_start = place
            elif data[place] == "[":
                second_start = place
            elif data[place] == ")":
                if second_end == -1 and second_start != -1:
                    error = "Error. No closing brackets to [."
                elif first_start == -1:
                    error = "Error. No opening bracket for )."
                else:
                    articles, words = self.parse_brackets(data[first_start+1:place],first_start, second_start, second_end)
                    wordlist = set(list(wordlist) + list(words))
                    if first_result_flag:
                        results = articles
                        first_result_flag = False
                    else:
                        if second_start > -1:
                            operator = self.find_operator(data, second_start, second_end)
                        else:
                            operator = self.find_operator(data, first_start, place)
                        results = self.filter_articles(results, articles, operator)
                    first_start = -1
                    self.first_not_flag = False
                    second_start, second_end = -1, -1
            elif data[place] == "]":
                if second_start == -1:
                    error = "No opening bracket for ]."
                second_end = place
                articles, words = self.parse_brackets(data[second_start:place], first_start, second_start)
                if first_result_flag:
                    results = articles
                    first_result_flag = False
                else:
                    wordlist = set(list(wordlist) + list(words))
                    operator = self.find_operator(data, second_start, second_end)
                    results = self.filter_articles(results, articles, operator)
                self.second_not_flag = False

        if first_result_flag:
            results, words = self.parse_brackets(data, 0)
            wordlist = set(list(wordlist) + list(words))
        wordlist = list(wordlist)
        return render(request, 'search/results.html', {"results": results, "error": error, "keywords": wordlist,
                                                       "searcher": ResultsView.searches,
                                                       "search": ResultsView.searches[len(ResultsView.searches)-1]})

    def clean_string(str):
        str = str.replace("^", "")
        str = str.replace("[", "")
        str = str.replace("]", "")
        str = str.replace("(", "")
        str = str.replace(")", "")
        return str

    def parse_brackets(self, data, first_start, second_start=-1, second_end=-1):

        if second_end > -1:
            data = data[:second_start] + data[second_end + 1:]
        data = AdvanceSearch.clean_string(data)

        words = re.split("&&|&|\|\|", data)

        if data.find("&&") > -1:
            article = self.get_and_articles(words, first_start, second_start)
        elif data.find("&") > -1:
            return self.get_easy_and_articles(words, first_start, second_start)
        else:
            article = self.get_or_articles(words, first_start, second_start)
        return article

    def get_and_articles(self, wordlist, first_start, second_start):
        # delete empty strings
        wordlist = [word for word in wordlist if word]
        if (second_start > -1 and self.second_not_flag) or \
                (first_start > -1 and self.first_not_flag):
            return ResultsView.not_statement(wordlist, "and"), wordlist

        return ResultsView.and_statement(wordlist), wordlist

    def get_easy_and_articles(self, wordlist, first_start, second_start):
        # delete empty strings
        wordlist = [word for word in wordlist if word]
        if (second_start > -1 and self.second_not_flag) or \
                (first_start > -1 and self.first_not_flag):
            return ResultsView.not_statement(wordlist, "easy-and"), wordlist

        return ResultsView.easy_and_statement(wordlist), wordlist

    def get_or_articles(self, wordlist, first_start, second_start):
        # delete empty strings
        wordlist = [word for word in wordlist if word]
        if (second_start > -1 and self.second_not_flag) or \
                (first_start > -1 and self.first_not_flag):
            return ResultsView.not_statement(wordlist, "or"), wordlist

        articles = ResultsView.or_statement(wordlist), wordlist
        return articles

    def find_operator(self, data, start, end):
        if data[start-1] == '^':
            start -= 1
        if (start > 2 and data[start-1] == '&' and data[start-2] == '&') or\
                (end+2 < len(data) and data[end+1] == '&' and data[end+2]):
            return "and"
        elif (start > 1 and data[start-1] == '&') or\
                (end+1 < len(data) and data[end+1] == '&'):
            return "easy-and"
        elif (start > 2 and data[start-1] == '|' and data[start-2] == '|') or \
                (end+2 < len(data) and data[end+1] == '|' and data[end+2] == '|'):
            return "or"

    def filter_articles(self, results, articles, operator):
        final_results = []
        if operator == "and":
            final_results = set(results) & set(articles)
        elif operator == "or":
            final_results = set(results) - set(articles)
        elif operator == "easy-and":
            max_list = results if len(results) >= len(articles) else articles
            min_list = results if len(results) < len(articles) else articles

            if len(set(max_list) & set(min_list)) < 0.6 * len(max_list):
                final_results = set(max_list) & set(min_list)
        return final_results



