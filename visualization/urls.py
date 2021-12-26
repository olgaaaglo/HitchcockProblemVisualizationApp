from django.urls import path

from . import views

app_name = 'visualization'

urlpatterns = [
    path('', views.index, name='index'),
    path('find/<str:city>', views.find, name='find')
]