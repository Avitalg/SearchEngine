from urllib.parse import urlparse
import re
from django.core.exceptions import ObjectDoesNotExist
import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from search.models import Article, Word, Postingfile as Pfile
from django.views import generic
import os
# coding: utf-8


class FindFilesView(generic.ListView):
    model = Article
    context_object_name = 'all_articles'
    url = 'http://shakespeare.mit.edu/Poetry/sonnets.html'
    amount = 4

    def get_context_data(self, **kwargs):
        context = super(FindFilesView, self).get_context_data(**kwargs)
        articles = self.crawling_url(self.url, self.amount)

        if not articles:
            context['error_msg'] = "No new articles was found"
        context['all_articles'] = articles
        return context

    def post(self, request):
        url = request.POST.get('url', self.url)
        narticles = request.POST.get("narticles", "4")
        narticles = int(narticles)
        self.url = url
        self.amount = narticles
        articles = self.crawling_url(url, narticles)
        return render(request, "search/results.html", {'results': articles})

    def crawling_url(self, url, article_number):
        split_url = url.rsplit('/', 1)
        url_domain = split_url[0]
        r = requests.get(url)
        html_content = r.text
        soup = BeautifulSoup(html_content)
        links = soup.find_all('a', href=True)
        hrefs = []
        for a in links:
            o = urlparse(a["href"])
            if not o.scheme:
                if a["href"] and not a["href"][0] == '/':
                    a["href"] = url_domain + '/' + a["href"]
                else:
                    a["href"] = url_domain + a["href"]
            if urlparse(a["href"]).netloc != urlparse(url_domain).netloc:
                print("continue")
                continue
            print("ok")
            hrefs.append(a["href"])
        hrefs = set(hrefs[:article_number])

        articles = FindFilesView.save_articles(hrefs)
        return articles

    def save_articles(links):
        articles = list()
        for link in links:
            if not FindFilesView.check_if_url_exists(link):
                r = requests.get(link)
                if r.status_code == 200:
                    html_content = r.content
                    soup = BeautifulSoup(html_content)
                    # clear script and style elements
                    for script in soup(["script", "style"]):
                        script.extract()

                    title = soup.title.string
                    text = soup.body.get_text()
                    filename = 'media/' + title + '.txt'
                    file = open(filename, 'w')
                    file.write(text)
                    file.close()

                    file = open(filename, 'r')
                    text = file.read()
                    print(text)
                    # break into lines and remove leading and trailing space on each
                    lines = (line.strip() for line in text.splitlines())
                    # break multi-headlines into a line each
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    # drop blank lines
                    text = '\n'.join(chunk for chunk in chunks if chunk)

                    regex = re.compile(r'[\n\r\t]')
                    text = text.rstrip()
                    text = regex.sub(' ', text)

                    summary = text[:300]
                    article = Article(title=title, summary=summary, url=link)
                    article.save()
                    articles.append(article)
                    article = Article.objects.get(pk=article.pk)
                    FindFilesView.save_words(article, text)
                    file.close()
                    os.remove(filename)

        return articles

    def save_words(article, text):
        word_list = re.findall(r"[\w']+", text)
        word_list = [word.lower() for word in word_list]
        word_list.sort()

        for word in word_list:
            print(word)
            try:
                new_word = Word.objects.get(data=word, article=article)
                new_word.amount += 1
                new_word.save()
            except (ObjectDoesNotExist, Word.DoesNotExist):
                new_word = Word()
                new_word.article = article
                new_word.data = word
                new_word.amount = 1
                new_word.save()
            finally:
                try:
                    pfile_word = Pfile.objects.get(data=word)
                    pfile_word.words.add(new_word)
                    pfile_word.save()
                except (ObjectDoesNotExist, Word.DoesNotExist):
                    pfile_word = Pfile(data=word)
                    pfile_word.save()
                    pfile_word.words.add(new_word)

    def check_if_url_exists(url):
        return Article.objects.filter(url=url).exists()

