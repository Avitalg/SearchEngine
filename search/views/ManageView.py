from search.models import Article, Word
from django.views import generic
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import sys
from urllib.parse import urlparse
import re
from django.core.exceptions import ObjectDoesNotExist
import requests
from bs4 import BeautifulSoup

class ManageView(generic.TemplateView):
    template_name = 'manage/index.html'


class AddFileView(generic.TemplateView):
    template_name = 'manage/addFiles.html'

    def post(self, request):
        files = request.FILES.getlist('files')

        if not files:
            result = "You need to enter a file."
        else:
            result = "Files uploaded successfully"

        try:
            for file in files:
                new_file = Article(file=file, hide=False)
                new_file.save()
        except:
                result = sys.exc_info()[0]

        return render(request, 'manage/submit.html', {'result': result})


class FindFilesView(generic.ListView):
    model = Article
    context_object_name = 'all_articles'

    def get_context_data(self, **kwargs):
        context = super(FindFilesView, self).get_context_data(**kwargs)

        url_domain = 'http://shakespeare.mit.edu/Poetry'
        url = url_domain + '/sonnets.html'

        r = requests.get(url)
        html_content = r.text
        soup = BeautifulSoup(html_content)
        articles = list()
        links = soup.find_all('a', href=True)
        hrefs = []
        for a in links:
            o = urlparse(a["href"])
            if not o.scheme:
                if not a["href"][0] == '/':
                    a["href"] = url_domain + '/' + a["href"]
                else:
                    a["href"] = url_domain + a["href"]
            if urlparse(a["href"]).netloc != urlparse(url_domain).netloc:
                print("continue")
                continue
            print("ok")
            hrefs.append(a["href"])

        hrefs = set(hrefs[:4])

        for link in hrefs:
            r = requests.get(link)
            if r.status_code == 200:
                html_content = r.text
                soup = BeautifulSoup(html_content)
                title = soup.title.string
                text = soup.body.get_text()
                regex = re.compile(r'[\n\r\t]')
                text = text.rstrip()
                text = regex.sub(' ', text)
                summary = text[:300]
                article = Article(title=title, summary=summary, url=link)
                article.save()
                articles.append(article)
                article = Article.objects.get(pk=article.pk)
                self.save_words_data(article, text)

        context['all_articles'] = articles
        return context

    def save_words_data(self, article, text):
        word_list = re.findall(r"[\w']+", text)
        word_list = [word.lower() for word in word_list]
        word_list.sort()

        for word in word_list:
            try:
                exist_word = Word.objects.get(data=word, article=article)
                exist_word.amount += 1
                exist_word.save()
            except (ObjectDoesNotExist, Word.DoesNotExist):
                new_word = Word()
                new_word.article = article
                new_word.data = word
                new_word.amount = 1
                new_word.save()
