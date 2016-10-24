from urllib.parse import urlparse
import re
from django.core.exceptions import ObjectDoesNotExist
import requests
from bs4 import BeautifulSoup
from search.models import Article, Word
from django.views import generic


class FindFilesView(generic.ListView):
    model = Article
    context_object_name = 'all_articles'

    def get_context_data(self, **kwargs):
        context = super(FindFilesView, self).get_context_data(**kwargs)

        url_domain = 'http://shakespeare.mit.edu/Poetry'
        url = url_domain + '/sonnets.html'

        articles = self.crawling_url(url, 8)
        if not articles:
            context['error_msg'] = "No new articles was found"
        context['all_articles'] = articles
        return context

    def post(self, request):
        url = request.POST.get('url', "")
        self.crawling_url(url, 4)

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
                if not a["href"][0] == '/':
                    a["href"] = url_domain + '/' + a["href"]
                else:
                    a["href"] = url_domain + a["href"]
            if urlparse(a["href"]).netloc != urlparse(url_domain).netloc:
                print("continue")
                continue
            print("ok")
            hrefs.append(a["href"])
        hrefs = set(hrefs[:article_number])

        articles = self.save_articles(hrefs)
        return articles

    def save_articles(self, links):
        articles = list()
        for link in links:
            if not self.check_if_url_exists(link):
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
                    FindFilesView.save_words(article, text)
        return articles

    def save_words(article, text):
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

    def check_if_url_exists(self, url):
        return Article.objects.filter(url=url).exists()

