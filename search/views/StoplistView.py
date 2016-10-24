from ..models import Article, Stoplist
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render


class AddToStoplistView(generic.edit.CreateView):
    model = Stoplist
    fields = ['data']

    def get_context_data(self, **kwargs):
        context = super(AddToStoplistView, self).get_context_data(**kwargs)
        context['error_msg'] = "No articles was found"
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.get('data', "")

        try:
            Stoplist.objects.get(data=data)
            result = "Word already in the list"
        except ObjectDoesNotExist:
            new_word = Stoplist(data=data)
            new_word.save()
            result = "Word added to the list"

        return render(request, 'manage/submit.html', {'result': result})


class StoplistView(generic.ListView):
    model = Article
    template_name = 'manage/stoplist_view.html'
    context_object_name = 'all_words'

    def get_context_data(self, **kwargs):
        context = super(StoplistView, self).get_context_data(**kwargs)
        context['error_msg'] = "Stoplist is empty"
        return context

    def get_queryset(self):
        print("error")
        return Stoplist.objects.all()

    def post(self, request, *args, **kwargs):
        id = int(request.POST.get('id', "1"))
        print(id)
        try:
            Stoplist.objects.get(id=id).delete()
            result = "Word deleted succesfully"
        except ObjectDoesNotExist:
            result = "The word doesn't exist in the stoplist"

        return render(request, 'manage/submit.html', {"result": result})
