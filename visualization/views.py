from django.shortcuts import render
#from django.http import HttpResponse, HttpResponseRedirect
import osmnx as ox
import networkx as nx
from OSMPythonTools.nominatim import Nominatim
from django.http import JsonResponse
#import plotly.graph_objects as go
#import numpy as np
import random as rnd
from subprocess import Popen

def index(request):
    return render(request, 'visualization/index.html')

coords = []

def find(request):
    try:
        city = request.POST['city']
        nominatim = Nominatim()
        place = nominatim.query(city)

        graph_area = (place.displayName())
        G = ox.graph_from_place(graph_area, network_type='drive')

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

        input_file = open("input.txt", "a")
        input_file.write(str(adj_list))
        input_file.write("\n")
        input_file.write(str(shops))
        input_file.write(str(warehouses))
        input_file.close()

        Popen(['./a.out'])

        output_file = open("output.txt", "r")
        print(output_file.read())
        output_file.close() 

        global coords
        coords = []
        for i in range(len(shops)):
            print(G.nodes()[shops[i]])
            coords.append(map(G.nodes()[shops[i]], G.nodes()[warehouses[i]], G, shops[i], warehouses[i]))
        return render(request, 'visualization/index.html', {'shops_nr' : shops_nr})
        #return render(request, 'visualization/index.html', {})
    except (TypeError):
        return render(request, 'visualization/index.html', {
            'error_message': "Nie podano miasta.",
        })

def result(request):
    global coords
    return JsonResponse({"coords" : coords})

def map(place1, place2, G, shop, warehouse):

    origin_point = (float(place1["x"]), float(place1["y"]))
    destination_point = (float(place2["x"]), float(place2["y"]))
    origin_node = shop
    destination_node = warehouse

    print(origin_point)
    print(destination_point)    
    
    print(origin_node)
    print(destination_node)

    route = nx.shortest_path(G, origin_node, destination_node, weight = 'length') #potem nie będzie potrzebne

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

    return {'lon': long, 'lat': lat}