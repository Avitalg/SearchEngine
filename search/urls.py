from django.conf.urls import url
from . import views


app_name = 'search'

urlpatterns = [
    #/search/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /search/71/
    url(r'^(?P<pk>[0-9]+)$', views.DetailView.as_view(), name='details'),
    url('articles/', views.ArticlesView.as_view(), name='articles'),
    url('results/', views.ResultsView.as_view(), name='results'),
    url('manage/', views.ManageView.as_view(), name='manage'),
    url(r'^article/add/$', views.AddFileView.as_view(), name='add-files'),
    url(r'^submit', views.AddFileView.as_view(), name='addFilesSubmit'),
]
