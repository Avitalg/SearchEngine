from ..models import Article
from django.views import generic


class ArticlesView(generic.ListView):
    model = Article
    template_name = 'search/articles.html'
    context_object_name = 'all_articles'

    def get_queryset(self):
        return Article.objects.all()