from ..models import Article, Word, Postingfile
from django.views import generic
import requests
from bs4 import BeautifulSoup
import re
from .FindFilesView import FindFilesView
import os


class UpdateFilesView(generic.ListView):
    model = Article
    template_name = 'search/article_list.html'
    context_object_name = 'all_articles'

    def get_context_data(self, **kwargs):
        context = super(UpdateFilesView, self).get_context_data(**kwargs)
        context['error_msg'] = "No articles was found"
        context['all_articles'] = self.update_files()
        return context

    def update_files(self):
        articles = Article.objects.all()
        updated_articles = list()
        for article in articles:
            data = UpdateFilesView.get_new_article_data(article.get_url())
            if data:
                article.title = data["title"]
                article.summary = data["summary"]
                text = data["text"]
                UpdateFilesView.delete_exist_words(article)
                FindFilesView.save_words(article, text)
                updated_articles.append(article)
        return updated_articles

    def get_new_article_data(link):
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
            file.close()
            os.remove(filename)
            return {"title": title, "summary": summary, "text": text}
        else:
            Article.objects.filter(url=link).delete()

    def delete_exist_words(article):
        Word.objects.filter(article=article).delete()
        Postingfile.objects.filter(words__isnull=True).delete()

