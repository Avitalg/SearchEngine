from django.conf.urls import url
from . import views


app_name = 'search'

urlpatterns = [
    #/search/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /search/71/
    url(r'^(?P<pk>[0-9]+)$', views.DetailView.as_view(), name='details'),
    url('manage/articles/', views.ArticlesManageView.as_view(), name='articles-manage'),
    url('articles/', views.ArticlesView.as_view(), name='articles'),
    url('results/', views.ResultsView.as_view(), name='results'),
    url('manage/find/', views.FindFilesView.as_view(), name='find-files'),
    url('manage/update/', views.UpdateFilesView.as_view(), name='update-files'),
    url('manage/change/', views.ChangeFilesView.as_view(), name='change-files'),
    url('manage/delete/', views.DeleteFilesView.as_view(), name='delete-files'),
    url('manage/', views.ManageView.as_view(), name='manage'),

    # url(r'^submit', views.AddFileView.as_view(), name='addFilesSubmit'),
]
