from search.models import Article
from django.views import generic
from django.shortcuts import render


class ManageView(generic.TemplateView):
    template_name = 'manage/index.html'



