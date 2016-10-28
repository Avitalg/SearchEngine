from ..models import Article
from django.views import generic


class ArticlesView(generic.ListView):
    model = Article
    template_name = 'search/article_list.html'
    context_object_name = 'all_articles'

    def get_context_data(self, **kwargs):
        context = super(ArticlesView, self).get_context_data(**kwargs)
        context['error_msg'] = "No articles was found"
        return context

    def get_queryset(self):
        return Article.objects.all().exclude(hide=True)


class ArticlesManageView(generic.ListView):
    model = Article
    template_name = 'search/article_list.html'
    context_object_name = 'all_articles'

    def get_context_data(self, **kwargs):
        context = super(ArticlesManageView, self).get_context_data(**kwargs)
        context['error_msg'] = "No articles was found"
        return context

    def get_queryset(self):
        print("ok")
        return Article.objects.all()
