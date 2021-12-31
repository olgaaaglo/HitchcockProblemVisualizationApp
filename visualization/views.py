from django.shortcuts import render
import osmnx as ox
from OSMPythonTools.nominatim import Nominatim
from django.http import JsonResponse
import random as rnd
from subprocess import Popen

def index(request):
    return render(request, 'visualization/index.html')


def find(request, city):
    G = get_graph(city)

    shops_nr, warehouses_nr, shops, warehouses, shops_needs, warehouses_loads = randomize_places(G)

    write_to_file(G, shops, warehouses, shops_needs, warehouses_loads)

    routes, lengths, cargos = get_results(list(G.nodes()))

    nodes = list(G.nodes())

    results = []
    for i, route in enumerate(routes):
        results.append({
            "coords" : map(G, route),
            "length" : lengths[i],
            "cargo" : cargos[i],
            "shop" : nodes.index(route[0]) + 1,
            "warehouse" : nodes.index(route[len(route) - 1]) + 1
        })
        
    input_data = {'shops_nr' : shops_nr, 'warehouses_nr' : warehouses_nr, 
                    'shops' : [nodes.index(shop) + 1 for shop in shops], 
                    'warehouses' : [nodes.index(warehouse) + 1 for warehouse in warehouses],
                    'shops_needs' : shops_needs, 'warehouses_loads' : warehouses_loads}
    
    return JsonResponse({'results' : results, 'input_data' : input_data})

def get_graph(city):
    nominatim = Nominatim()
    place = nominatim.query(city)

    graph_area = (place.displayName())
    G = ox.graph_from_place(graph_area, network_type='drive')

    return G

def randomize_places(G):
    shops_nr = rnd.randint(4, 10)
    warehouses_nr = rnd.randint(4, 10)
    all = rnd.sample(G.nodes(), shops_nr + warehouses_nr)

    shops = all[:shops_nr]
    warehouses = all[shops_nr:]

    shops_needs = [rnd.randint(10, 40) * 10 for i in range(shops_nr)]
    warehouses_loads = [rnd.randint(10, 40) * 10 for i in range(warehouses_nr)]
    
    return shops_nr, warehouses_nr, shops, warehouses, shops_needs, warehouses_loads

def write_to_file(G, shops, warehouses, shops_needs, warehouses_loads):
    nodes = list(G.nodes())

    with open("input.txt", "w") as input_file:
        input_file.write(f'{ str(len(nodes)) }\n')

        for v in G.adj:
            input_file.write(f'{ str(nodes.index(v) + 1) }: ')
            for u, value in G.adj[v].items():
                input_file.write(f'{ str(nodes.index(u) + 1) } { str(value[0]["length"]) } ')
            input_file.write('\n')
            
        input_file.write('---\n')
        for i in range(len(shops)):
            input_file.write(f'{ str(nodes.index(shops[i]) + 1) } { str(shops_needs[i]) } ')

        input_file.write('\n---\n')
        for i in range(len(warehouses)):
            input_file.write(f'{ str(nodes.index(warehouses[i]) + 1) } { str(warehouses_loads[i]) } ')

        input_file.write('\n---')

def get_results(nodes):
    process = Popen(['./Hitchcock', 'input.txt'])
    process.wait()

    with open("output.txt", "r") as output_file:
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
        
        cargos = [cargo for cargo in cargos if cargo != '0']

    return results, lengths, cargos

def map(G, route):
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

        if best_edge != None and 'geometry' in best_edge[2]:
            x, y = best_edge[2]['geometry'].xy
            for k in range(len(x)):
                long.append(x[k])
                lat.append(y[k])
        else:
            long.append(point1['x'])
            lat.append(point1['y'])
            long.append(point2['x'])
            lat.append(point2['y'])

    return {'lon': long, 'lat': lat}