fetch(url, {
    method: 'GET',
    headers:{
        'Content-Type': 'application/json',
    },
})
.then(response => {
    result = response.json()
    status_code = response.status;
    if(status_code != 200) {
        console.log('Error in getting info!')
        return false;
    }
    
    return result
})
.then(data => {
    console.log(data);
    alldata = [];
    coords = data["coords"]
    lengths = data["lengths"]
    cargos = data["cargos"]
    shops = data['shops']
    shops_in_routes = data['shops_in_routes']
    warehouses_in_routes = data['warehouses_in_routes']
    
    colors = ["fuchsia", "blue", "green", "orange", "cyan", "purple", "black", "hotpink", "brown", "yellow"]

    for (var i = 0; i < coords.length; i++)
    {
        shop_color = colors[shops.indexOf(shops_in_routes[i])]

        var mapdata = {
                type: "scattermapbox",
                lon: coords[i]['lon'],
                lat: coords[i]['lat'],
                marker: { color: shop_color, size: 5 },
                mode: "lines",
                text: "Length: " + lengths[i] + ", Cargo: " + cargos[i],
                name: "Route " + warehouses_in_routes[i] + "-" + shops_in_routes[i]
        };

        var shop = {
            type: "scattermapbox",
            lon: [coords[i]['lon'][0]],
            lat: [coords[i]['lat'][0]],
            marker: { 'size': 12, 'color':shop_color },
            mode: "markers",
            text:['Sklep'],
            name: shops_in_routes[i]
        };

        var routeLen = coords[i]['lon'].length;
        var warehouse = {
            type: "scattermapbox",
            lon: [coords[i]['lon'][routeLen - 1]],
            lat: [coords[i]['lat'][routeLen - 1]],
            marker: { 'size': 12, 'color':"red" },
            mode: "markers",
            text:['Magazyn'],
            name: warehouses_in_routes[i]
        };

        alldata.push(mapdata)
        alldata.push(shop)
        alldata.push(warehouse)
    }

    console.log(alldata);
    var reducer = (a, b) => (a + b)
        
    var layout = {
        autosize: false,
        width: 1000,
        height: 500,
        dragmode: "zoom",
        mapbox: { 
                style: "open-street-map", 
                center: { 
                            lat: coords[0]['lat'].reduce(reducer)/coords[0]['lat'].length, 
                            lon: coords[0]['lon'].reduce(reducer)/coords[0]['lon'].length 
                        },
                zoom: 13 
                },
        margin: { r: 0, t: 0, b: 0, l: 0 }
    };
    
    Plotly.newPlot("div1", alldata, layout);
})
.catch(error => {
    console.log(error)
})