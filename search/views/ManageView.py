from ..models import Article
from django.views import generic
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import sys


class ManageView(generic.TemplateView):
    template_name = 'manage/index.html'


class AddFileView(generic.TemplateView):
    template_name = 'manage/addFiles.html'

    def post(self, request):
        files = request.FILES.getlist('files')

        if not files:
            result = "You need to enter a file."
        else:
            result = "Files uploaded successfully"

        try:
            for file in files:
                new_file = Article(file=file, hide=False)
                new_file.save()
        except:
                result = sys.exc_info()[0]

        return render(request, 'manage/submit.html', {'result': result})
