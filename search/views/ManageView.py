from ..models import Article
from django.views import generic
from django.shortcuts import render


class ManageView(generic.TemplateView):
    template_name = 'manage/index.html'


class AddFileView(generic.TemplateView):
    template_name = 'manage/addFiles.html'


def addFilesSubmit(request):
    files = request.FILES.getlist('files')

    for file in files:
        new_file = Article(file=file, hide=False)
        new_file.save()

    return render(request, 'manage/submit.html', {'result': 'result!!!'})