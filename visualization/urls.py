from django.urls import path

from . import views

app_name = 'visualization'

urlpatterns = [
    path('', views.index, name='index'),
    path('find/', views.find, name='find'),
    path('result/', views.result, name='result'),
]