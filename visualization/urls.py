from django.urls import path

from . import views

app_name = 'visualization'

urlpatterns = [
    path('', views.index, name='index'),
    path('find/<str:city>/<int:shops_nr>/<int:warehouses_nr>', views.find, name='find'),
    path('get_results_to_redraw/<int:simulatedAnnealing>', views.get_results_to_redraw, name='get_results_to_redraw')
]