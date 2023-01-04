from django.urls import path
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path('overview/count', views.overview.count),
    path('book/list', views.book.list_api),
    path('book/detail', views.book.detail),
    path('book/create', views.book.create),
    path('book/update', views.book.update),
    path('book/delete', views.book.delete),
    path('comment/list', views.comment.list_api),
    path('comment/create', views.comment.create),
    path('comment/update', views.comment.update),
    path('comment/delete', views.comment.delete),
    path('classification/list', views.classification.list_api),
    path('classification/create', views.classification.create),
    path('classification/update', views.classification.update),
    path('classification/delete', views.classification.delete),
    path('tag/list', views.tag.list_api),
    path('tag/create', views.tag.create),
    path('tag/update', views.tag.update),
    path('tag/delete', views.tag.delete),
    path('record/list', views.record.list_api),
    path('record/create', views.record.create),
    path('record/update', views.record.update),
    path('record/delete', views.record.delete),
    path('user/list', views.user.list_api),
    path('user/create', views.user.create),
    path('user/update', views.user.update),
    path('user/updatePwd', views.user.updatePwd),
    path('user/delete', views.user.delete),
]
