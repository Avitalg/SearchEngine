from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'search/index.html'


class HelpView(TemplateView):
    template_name = 'search/help.html'
