from django.conf.urls import url
from . import views
from django.conf.urls import (
handler400, handler403, handler404, handler500
)


handler404 = 'search.views.handler404'
handler500 = 'search.views.handler500'


app_name = 'search'

urlpatterns = [
    url('articles/', views.ArticlesView.as_view(), name='articles'),
    url(r'^advance-search/$', views.AdvanceSearch.as_view(), name='advance-search'),
    url(r'^advance/results/', views.AdvanceSearch.as_view(), name='advance-results'),
    url('results/', views.ResultsView.as_view(), name='results'),
    url('manage/articles/', views.ArticlesManageView.as_view(), name='articles-manage'),
    url('manage/find/', views.FindFilesView.as_view(), name='find-files'),
    url('manage/update/', views.UpdateFilesView.as_view(), name='update-files'),
    url('manage/postingfile/', views.PostingfileView.as_view(), name='postingfile'),
    url('manage/change/', views.ChangeFilesView.as_view(), name='change-files'),
    url('manage/delete/', views.DeleteFilesView.as_view(), name='delete-files'),
    url('manage/stoplist/view/', views.StoplistView.as_view(), name='stoplist-view'),
    url('manage/stoplist/add/', views.AddToStoplistView.as_view(), name='stoplist-words'),
    url('manage/files/', views.ManageFilesView.as_view(), name='manage-files'),
    url('manage/stoplist/', views.ManageStoplistView.as_view(), name='manage-stoplist'),
    url('manage/settings/find/', views.SettingsView.as_view(), name='manage-settings'),
    url('manage/settings/', views.FindFilesView.as_view(), name='manage-new-files'),
    url('manage/', views.ManageView.as_view(), name='manage'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)$', views.DetailView.as_view(), name='details'),

    # url(r'^submit', views.AddFileView.as_view(), name='addFilesSubmit'),
]

