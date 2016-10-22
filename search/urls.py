from django.conf.urls import url
from . import views


app_name = 'search'

urlpatterns = [
    #/search/
    url(r'^$', views.index, name='index'),
    # /search/71/
    url(r'^(?P<article_id>[0-9]+)$', views.details, name='details'),
    url('articles/', views.articles, name='articles'),
    url('results/', views.results, name='results'),
    url('manage/', views.manage, name='manage'),
    url(r'^addFiles$', views.addFiles, name='addFiles'),
    url(r'^submit', views.addFilesSubmit, name='addFilesSubmit'),
]
