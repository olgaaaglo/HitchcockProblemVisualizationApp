from django.shortcuts import render
import osmnx as ox
import networkx as nx
from OSMPythonTools.nominatim import Nominatim
from django.http import JsonResponse
import random as rnd
from subprocess import Popen

def index(request):
    return render(request, 'visualization/index.html')

results = {}

def find(request):
    #try:
        G = get_graph(request.POST['city'])

        print(len(G.nodes()))
        #print(G.adj)

        shops_nr, warehouses_nr, shops, warehouses, shops_needs, warehouses_loads = randomize_places(G)

        write_to_file(G, shops, warehouses, shops_needs, warehouses_loads)

        routes, lengths, cargos = get_results(list(G.nodes()), G)

        global results
        results["coords"] = []
        results["lengths"] = lengths
        results["cargos"] = cargos
        ####################################
        #shops = [17, 99, 383, 235, 338]
        shops = [303, 161, 131, 168, 328, 260, 255]
        nodes = list(G.nodes())
        results["shops"] = shops #[nodes.index(shop) + 1 for shop in shops]
        results["shops_in_routes"] = [nodes.index(route[0]) + 1 for route in routes]
        results["warehouses_in_routes"] = [nodes.index(route[len(route) - 1]) + 1 for route in routes]

        # for i in range(len(shops)):
        #     print(G.nodes()[shops[i]])
        #     coords.append(map(G, shops[i], warehouses[i]))
        # coords.append(map(G, shops[0], warehouses[1]))
        # coords.append(map(G, shops[1], warehouses[1]))
        # coords.append(map(G, shops[2], warehouses[0]))
        for route in routes:
            results["coords"].append(map(G, route))
        return render(request, 'visualization/index.html', {'shops_nr' : shops_nr, 'warehouses_nr' : warehouses_nr})
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
    shops_nr = rnd.randint(4, 10)
    warehouses_nr = rnd.randint(4, shops_nr)
    all = rnd.sample(G.nodes(), shops_nr + warehouses_nr)

    shops = all[:shops_nr]
    warehouses = all[shops_nr:]

    #print(shops)
    #print(warehouses)

    shops_needs = []
    warehouses_loads = []

    for i in range(shops_nr):
        shops_needs.append(rnd.randint(10, 40) * 10)
    for i in range(warehouses_nr):
        warehouses_loads.append(rnd.randint(10, 40) * 10)
    
    return shops_nr, warehouses_nr, shops, warehouses, shops_needs, warehouses_loads

def write_to_file(G, shops, warehouses, shops_needs, warehouses_loads):
    nodes = list(G.nodes())

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

def get_results(nodes, G):
    Popen(['./a.out'])

    output_file = open("out1.txt", "r")
    output = output_file.read().split('\n---\n')
    routes = output[0]
    cargos = output[1].split('\n')

    results = []
    lengths = []
    for count, route in enumerate(routes.split('\n')):
        if cargos[count] != '0':
            array = route.split()
            results.append([nodes[int(i) - 1] for i in array[:len(array) - 1]])
            lengths.append(float(array[len(array) - 1]))
        
        # if int(array[0]) == 383 and int(array[len(array) - 2]) == 327:
        #     print(array[len(array) - 2])
        #     print(G.nodes[nodes[int(array[0]) - 1]]['x'])
        #     print(nodes[int(array[0]) - 1])
        #     print(nodes[int(array[len(array) - 2]) - 1])
    
    cargos = [cargo for cargo in cargos if cargo != '0']

    output_file.close()

    return results, lengths, cargos

def result(request):
    global results
    return JsonResponse(results)

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
    #print("route in map() " + str(route))

    if route[0] == 2763834671 and route[len(route) - 1] == 2181202348: 
        print([G.nodes[r]['x'] for r in route])

    long = [] 
    lat = []  
    for i in range(len(route) - 1):
        point1 = G.nodes[route[i]]
        point2 = G.nodes[route[i+1]]

        best_edge = None
        for j in list(G.edges(data=True)):
            if (j[0]==route[i]) and (j[1]==route[i+1]):
                if best_edge == None or best_edge[2]['length'] > j[2]['length']:
                    best_edge = j
        if best_edge == None:
            long.append(point1['x'])
            lat.append(point1['y'])
            long.append(point2['x'])
            lat.append(point2['y'])
        else:
            if 'geometry' in best_edge[2]:
                x, y = best_edge[2]['geometry'].xy
                if route[0] == 2763834671 and route[len(route) - 1] == 2181202348: 
                    print("xxxxxxxxxxxxxxx")
                    print(x)
                for k in range(len(x)):
                    long.append(x[k])
                    lat.append(y[k])
            else:
                print('no geometry')
                long.append(point1['x'])
                lat.append(point1['y'])
                long.append(point2['x'])
                lat.append(point2['y'])


    if(route[0] == 2763834671)  and route[len(route) - 1] == 2181202348:
        print(long)
        print(lat)

    return {'lon': long, 'lat': lat}