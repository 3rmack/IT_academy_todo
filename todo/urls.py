from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'add_task', views.add_task, name='add_task'),
    url(r'', views.index, name='index'),

]
