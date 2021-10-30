from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import osmnx as ox
import networkx as nx
from datetime import timedelta
from OSMPythonTools.nominatim import Nominatim
from django.http import JsonResponse

def index(request):
    context = {
        'input': 'hmm',
    }
    return render(request, 'visualization/index.html', context)

def find(request):
    # try:
    #     selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    #     return render(request, 'polls/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a choice.",
    #     })

    # address1 = request.POST['address1']
    # address2 = request.POST['address2']
    # nominatim = Nominatim()
    # place1 = nominatim.query(address1)
    # place2 = nominatim.query(address2)

    # graph_area = ("Kraków, Polska")

    # # Create the graph of the area from OSM data. It will download the data and create the graph
    # G = ox.graph_from_place(graph_area, network_type='drive')

    # # OSM data are sometime incomplete so we use the speed module of osmnx to add missing edge speeds and travel times
    # G = ox.add_edge_speeds(G)
    # G = ox.add_edge_travel_times(G)

    # origin_coordinates = (float(place1.toJSON()[0]["lat"]), float(place1.toJSON()[0]["lon"]))
    # destination_coordinates = (float(place2.toJSON()[0]["lat"]), float(place2.toJSON()[0]["lon"]))

    # origin_node = ox.get_nearest_node(G, origin_coordinates)
    # destination_node = ox.get_nearest_node(G, destination_coordinates)

    # distance_in_meters = nx.shortest_path_length(G, origin_node, destination_node, weight='length')
    # distance_in_kilometers = distance_in_meters / 1000


    # context = {'places': [ {'name': place1.displayName(),
    #         'osmId': place1.toJSON()[0]["osm_id"],
    #         'latitude': place1.toJSON()[0]["lat"],
    #         'longitude': place1.toJSON()[0]["lon"]},
    #         {'name': place2.displayName(),
    #         'osmId': place2.toJSON()[0]["osm_id"],
    #         'latitude': place2.toJSON()[0]["lat"],
    #         'longitude': place2.toJSON()[0]["lon"]}
    #     ],
    #     'distance': distance_in_kilometers
    # }

    # for place in context['places']:
    #     print(place['name'])
    #return HttpResponseRedirect(reverse('visualization:result', args=(address,)))
    #return render(request, 'visualization/index.html', context)
    return render(request, 'visualization/index.html', JsonResponse({'test' : 'TEST'}))

def result(request):
    
    return JsonResponse({'test' : 'TEST'})