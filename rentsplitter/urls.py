from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^expense$', views.expense, name='expense'),
    url(r'^delete$', views.delete, name='delete'),
]
