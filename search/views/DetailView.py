from ..models import Article
from django.views import generic


class DetailView(generic.DetailView):
    model = Article
    template_name = 'search/detail.html'

