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
    data = data["coords"]
    
    colors = ["fuchsia", "red", "blue", "green", "orange", "yellow", "cyan", "purple", "black", "pink"]
    console.log(data.length);

    for (var i = 0; i < data.length; i++)
    {
        var mapdata = {
                type: "scattermapbox",
                lon: data[i]['lon'],
                lat: data[i]['lat'],
                marker: { color: colors[i], size: 5 },
                mode: "lines"
        };

        var shop = {
            type: "scattermapbox",
            lon: [data[i]['lon'][0]],
            lat: [data[i]['lat'][0]],
            marker: { 'size': 12, 'color':"red" },
            mode: "markers",
            text:['Sklep']
        };

        var routeLen = data[i]['lon'].length;
        var warehouse = {
            type: "scattermapbox",
            lon: [data[i]['lon'][routeLen - 1]],
            lat: [data[i]['lat'][routeLen - 1]],
            marker: { 'size': 12, 'color':"green" },
            mode: "markers",
            text:['Magazyn']
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
                            lat: data[0]['lat'].reduce(reducer)/data[0]['lat'].length, 
                            lon: data[0]['lon'].reduce(reducer)/data[0]['lon'].length 
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