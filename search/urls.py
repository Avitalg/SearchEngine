from django.conf.urls import url
from . import views


app_name = 'search'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)$', views.DetailView.as_view(), name='details'),
    url('articles/', views.ArticlesView.as_view(), name='articles'),
    url('results/', views.ResultsView.as_view(), name='results'),
    url('advance/', views.AdvanceSearch.as_view(), name='advance'),
    url('manage/articles/', views.ArticlesManageView.as_view(), name='articles-manage'),
    url('manage/find/', views.FindFilesView.as_view(), name='find-files'),
    url('manage/update/', views.UpdateFilesView.as_view(), name='update-files'),
    url('manage/change/', views.ChangeFilesView.as_view(), name='change-files'),
    url('manage/delete/', views.DeleteFilesView.as_view(), name='delete-files'),
    url('manage/stoplist/view/', views.StoplistView.as_view(), name='stoplist-view'),
    url('manage/stoplist/', views.AddToStoplistView.as_view(), name='stoplist-words'),
    url('manage/', views.ManageView.as_view(), name='manage'),

    # url(r'^submit', views.AddFileView.as_view(), name='addFilesSubmit'),
]
