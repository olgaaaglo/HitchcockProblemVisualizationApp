from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import osmnx as ox
import networkx as nx
from datetime import timedelta
from OSMPythonTools.nominatim import Nominatim
from django.http import JsonResponse
import plotly.graph_objects as go
import numpy as np
import random as rnd

def index(request):
    context = {
        'input': 'hmm',
    }
    return render(request, 'visualization/index.html', context)

coords = []

def find(request):
    try:
        city = request.POST['city']
        nominatim = Nominatim()
        place = nominatim.query(city)#.toJSON()[0]

        graph_area = (place.displayName())

        # Create the graph of the area from OSM data. It will download the data and create the graph
        G = ox.graph_from_place(graph_area, network_type='drive')

        # OSM data are sometime incomplete so we use the speed module of osmnx to add missing edge speeds and travel times
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)

        print(len(G.nodes()))
        #print(G.adj)

        adj_list = {}
        for v in G.adj:
            adj_list[v] = []
            for u, value in G.adj[v].items():
                adj_list[v].append({u : value[0]['length']})

        #print(adj_list)

        #fig, ax = ox.plot_graph(G, figsize=(10, 10), node_size=2, edge_color='y', edge_linewidth=0.2)

        shops_nr = rnd.randint(4, 10)
        #print(G.nodes())
        shops = rnd.sample(G.nodes(), shops_nr*2)
        warehouses = shops[len(shops)//2:]
        shops = shops[:len(shops)//2]
        print(shops)
        print(warehouses)

        global coords
        coords = []
        for i in range(len(shops)):
            print(G.nodes()[shops[i]])
            coords.append(map(G.nodes()[shops[i]], G.nodes()[warehouses[i]], G, shops[i], warehouses[i]))
        return render(request, 'visualization/index.html', {'shops_nr' : shops_nr})
        #return render(request, 'visualization/index.html', {})
    except (KeyError):
        # Redisplay the question voting form.
        return render(request, 'visualization/index.html', {
            'error_message': "You didn't select a choice.",
        })

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

def result(request):
    global coords
    return JsonResponse({"coords" : coords})

def map(place1, place2, G, shop, warehouse):
    # # Defining the map boundaries 
    # north, east, south, west = 33.798, -84.378, 33.763, -84.422  
    # # Downloading the map as a graph object 
    # G = ox.graph_from_bbox(north, south, east, west, network_type = 'drive')  
    # # Plotting the map graph 
    # #ox.plot_graph(G)

    # define origin and desination locations 
    # origin_point = (33.787201, -84.405076) 
    # destination_point = (33.764135, -84.394980)# get the nearest nodes to the locations 
    # origin_node = ox.get_nearest_node(G, origin_point) 
    # destination_node = ox.get_nearest_node(G, destination_point)# printing the closest node id to origin and destination points origin_node, destination_node

    origin_point = (float(place1["x"]), float(place1["y"]))
    destination_point = (float(place2["x"]), float(place2["y"]))
    origin_node = shop #ox.get_nearest_node(G, origin_point)
    destination_node = warehouse #ox.get_nearest_node(G, destination_point)

    print(origin_point)
    print(destination_point)    
    
    print(origin_node)
    print(destination_node)


    # Finding the optimal path 
    route = nx.shortest_path(G, origin_node, destination_node, weight = 'length') #potem nie będzie potrzebne

    # getting coordinates of the nodes# we will store the longitudes and latitudes in following list 
    long = [] 
    lat = []  
    for i in range(len(route) - 1):
        point1 = G.nodes[route[i]]
        point2 = G.nodes[route[i+1]]
        for j in list(G.edges(data=True)):
            if (j[0]==route[i]) and (j[1]==route[i+1]):
                if 'geometry' in j[2]:
                    x, y = j[2]['geometry'].xy
                    for k in range(len(x)):
                        long.append(x[k])
                        lat.append(y[k])
                else:
                    long.append(point1['x'])
                    lat.append(point1['y'])
                    long.append(point2['x'])
                    lat.append(point2['y'])


    # long = [] 
    # lat = []  
    # for i in route:
    #     point = G.nodes[i]
    #     long.append(point['x'])
    #     lat.append(point['y'])

    # print("lonlat")
    # print(long)
    # print(lat)

    #plot_path(lat, long, origin_point, destination_point)
    return {'lon': long, 'lat': lat}

# def plot_path(lat, long, origin_point, destination_point):
    
#     """
#     Given a list of latitudes and longitudes, origin 
#     and destination point, plots a path on a map
    
#     Parameters
#     ----------
#     lat, long: list of latitudes and longitudes
#     origin_point, destination_point: co-ordinates of origin
#     and destination    Returns
#     -------
#     Nothing. Only shows the map.
#     """    # adding the lines joining the nodes
#     fig = go.Figure(go.Scattermapbox(
#         name = "Path",
#         mode = "lines",
#         lon = long,
#         lat = lat,
#         marker = {'size': 10},
#         line = dict(width = 4.5, color = 'blue')))    # adding source marker
#     fig.add_trace(go.Scattermapbox(
#         name = "Source",
#         mode = "markers",
#         lon = [origin_point[1]],
#         lat = [origin_point[0]],
#         marker = {'size': 12, 'color':"red"}))
     
#     # adding destination marker
#     fig.add_trace(go.Scattermapbox(
#         name = "Destination",
#         mode = "markers",
#         lon = [destination_point[1]],
#         lat = [destination_point[0]],
#         marker = {'size': 12, 'color':'green'}))
    
#     # getting center for plots:
#     lat_center = np.mean(lat)
#     long_center = np.mean(long)    # defining the layout using mapbox_style
#     fig.update_layout(mapbox_style="stamen-terrain",
#         mapbox_center_lat = 30, mapbox_center_lon=-80)
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
#                       mapbox = {
#                           'center': {'lat': lat_center, 
#                           'lon': long_center},
#                           'zoom': 13})
#     fig.show()