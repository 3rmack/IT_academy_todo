from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'add_task', views.add_task, name='add_task'),
    url(r'updown', views.updown, name='updown'),
    url(r'edit', views.edit, name='edit'),
    url(r'delete', views.delete, name='delete'),
    url(r'', views.index, name='index'),
]
