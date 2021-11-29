from django.shortcuts import render
import osmnx as ox
import networkx as nx
from OSMPythonTools.nominatim import Nominatim
from django.http import JsonResponse
import random as rnd
from subprocess import Popen
import copy

def index(request):
    return render(request, 'visualization/index.html')

coords = []

def find(request):
    #try:
        G = get_graph(request.POST['city'])

        print(len(G.nodes()))
        #print(G.adj)

        shops_nr, shops, warehouses, shops_needs, warehouses_loads = randomize_places(G)

        write_to_file(G, shops, warehouses, shops_needs, warehouses_loads)

        routes = get_results()

        global coords
        coords = []
        # for i in range(len(shops)):
        #     print(G.nodes()[shops[i]])
        #     coords.append(map(G, shops[i], warehouses[i]))
        # coords.append(map(G, shops[0], warehouses[1]))
        # coords.append(map(G, shops[1], warehouses[1]))
        # coords.append(map(G, shops[2], warehouses[0]))
        for route in routes:
            coords.append(map(G, route))
        return render(request, 'visualization/index.html', {'shops_nr' : shops_nr})
        #return render(request, 'visualization/index.html', {})
    # except (TypeError):
    #     return render(request, 'visualization/index.html', {
    #         'error_message': "Nie podano miasta.",
    #     })

def get_graph(city):
    nominatim = Nominatim()
    place = nominatim.query(city)

    graph_area = (place.displayName())
    G = ox.graph_from_place(graph_area, network_type='drive')

    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    return G

def randomize_places(G):
    shops_nr = 3 #rnd.randint(4, 10)
    shops = rnd.sample(G.nodes(), shops_nr*2)

    warehouses = shops[len(shops)//2:] #czy magazynow moze byc wiecej niz sklepow
    shops = shops[:len(shops)//2]

    print(shops)
    print(warehouses)

    shops_needs = []
    warehouses_loads = []

    for i in range(len(shops)):
        shops_needs.append(rnd.randint(10, 40) * 10)
    for i in range(len(warehouses)):
        warehouses_loads.append(rnd.randint(10, 40) * 10)
    
    return shops_nr, shops, warehouses, shops_needs, warehouses_loads

def write_to_file(G, shops, warehouses, shops_needs, warehouses_loads):
    nodes = list(G.nodes()) #copy.deepcopy(list(G.nodes()))

    input_file = open("input.txt", "w")
    input_file.write(str(len(G.nodes())))
    input_file.write("\n")

    for v in G.adj:
        input_file.write(str(nodes.index(v) + 1) + ": ")
        for u, value in G.adj[v].items():
            input_file.write(str(nodes.index(u) + 1) + " " + str(value[0]['length']) + " ")
        input_file.write("\n")
        
    input_file.write("---\n")
    for i in range(len(shops)):
        input_file.write(str(nodes.index(shops[i]) + 1) + " " + str(shops_needs[i]) + " ")

    input_file.write("\n---\n")
    for i in range(len(warehouses)):
        input_file.write(str(nodes.index(warehouses[i]) + 1) + " " + str(warehouses_loads[i]) + " ")
    
    input_file.close()

def get_results():
    Popen(['./a.out'])

    output_file = open("output.txt", "r")
    routes = output_file.read()

    results = [[int(i) for i in route.split()] for route in routes.split('\n\n')] #jeszcze trzeba bedzie zamienic indeksowanie

    output_file.close()

    return results

def result(request):
    global coords
    return JsonResponse({"coords" : coords})

def map(G, route): #shop, warehouse):

    # place1 = G.nodes()[shop]
    # place2 = G.nodes()[warehouse]

    # origin_point = (float(place1["x"]), float(place1["y"]))
    # destination_point = (float(place2["x"]), float(place2["y"]))
    # origin_node = shop
    # destination_node = warehouse

    # print(origin_point)
    # print(destination_point)    
    
    # print(origin_node)
    # print(destination_node)

    # route = nx.shortest_path(G, origin_node, destination_node, weight = 'length') #potem nie będzie potrzebne
    print("route in map() " + str(route))

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