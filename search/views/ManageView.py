from search.models import Article, Postingfile
from django.views import generic
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count


class ManageView(generic.TemplateView):
    template_name = 'manage/index.html'


class ManageFilesView(generic.TemplateView):
    template_name = 'manage/manage-articles.html'


class ManageStoplistView(generic.TemplateView):
    template_name = 'manage/manage-stoplist.html'



class SettingsView(generic.TemplateView):
    template_name = 'manage/manage-settings.html'


class PostingfileView(generic.ListView):
    model = Postingfile
    template_name = 'manage/postingfile.html'
    context_object_name = 'results'

    def get_queryset(self):
        return Postingfile.objects.all().annotate(num_articles=Count('words')) \
                .order_by('-num_articles', 'data')


class ChangeFilesView(generic.ListView):
    model = Article
    template_name = 'manage/change_articles.html'
    context_object_name = "all_articles"

    def post(self, request):
        vis = request.POST.get('vis', "False")
        id = int(request.POST.get('article_id', "4"))
        print(id)
        print(vis)
        error = ["ok"]

        try:
            article = Article.objects.get(pk=id)
            article.hide = eval(vis)
            article.save()
        except ObjectDoesNotExist:
            error ="Either the entry or blog doesn't exist."

        return render(request, self.template_name, {'all_articles': Article.objects.all(), "error":error})


class DeleteFilesView(generic.TemplateView):
    template_name = 'manage/submit.html'
    context_object_name = 'result'

    def get_context_data(self, **kwargs):
        context = super(DeleteFilesView, self).get_context_data(**kwargs)
        Article.objects.filter(hide=True).delete()
        Postingfile.objects.filter(words__isnull=True).delete()
        context['result'] = "Hidden articles were deleted"
        return context
