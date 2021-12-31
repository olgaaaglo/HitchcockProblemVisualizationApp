function visualize() {
    const city = document.getElementById("city").value;

    fetch('/visualization/find/' + city,{
        method: 'GET',
        headers:{
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        const result = response.json()
        const status_code = response.status;
        if(status_code != 200) {
            console.log('Error in getting info!')
            return false;
        }
        
        return result
    })
    .then(data => {
        let divinfo = document.getElementById('divinfo')
        divinfo.innerHTML = 
        `<p>Wylosowano ` + data['input_data']['shops_nr'] + ` sklepów i ` + data['input_data']['warehouses_nr'] + ` magazynów. 
        Magazyny są zaznaczone kolorem czerwonym, a każdy sklep i trasy do niego tym samym innym kolorem.</p>`

        divinfo.innerHTML += getTables(data)

        console.log(data);
        let alldata = [];
        data = data["results"]
        
        const colors = ["fuchsia", "blue", "green", "orange", "cyan", "purple", "black", "hotpink", "brown", "yellow"]
        const shops = data.map((element) => element["shop"]).filter((value, index, self) => self.indexOf(value) === index)

        for (let i = 0; i < data.length; i++)
        {
            let shop_color = colors[shops.indexOf(data[i]["shop"])]

            let mapdata = {
                    type: "scattermapbox",
                    lon: data[i]["coords"]['lon'],
                    lat: data[i]["coords"]['lat'],
                    marker: { color: shop_color, size: 5 },
                    mode: "lines",
                    text: "Length: " + data[i]["length"] + ", Cargo: " + data[i]["cargo"],
                    name: "Route " + data[i]["warehouse"] + "-" + data[i]["shop"]
            };

            let shop = {
                type: "scattermapbox",
                lon: [data[i]["coords"]['lon'][0]],
                lat: [data[i]["coords"]['lat'][0]],
                marker: { 'size': 12, 'color':shop_color },
                mode: "markers",
                text:['Sklep'],
                name: data[i]["shop"]
            };

            let routeLen = data[i]["coords"]['lon'].length;
            let warehouse = {
                type: "scattermapbox",
                lon: [data[i]["coords"]['lon'][routeLen - 1]],
                lat: [data[i]["coords"]['lat'][routeLen - 1]],
                marker: { 'size': 12, 'color':"red" },
                mode: "markers",
                text:['Magazyn'],
                name: data[i]["warehouse"]
            };

            alldata.push(mapdata)
            alldata.push(shop)
            alldata.push(warehouse)
        }

        let reducer = (a, b) => (a + b)
            
        let layout = {
            autosize: false,
            width: 1000,
            height: 500,
            dragmode: "zoom",
            mapbox: { 
                    style: "open-street-map", 
                    center: { 
                                lat: data[0]["coords"]['lat'].reduce(reducer)/data[0]["coords"]['lat'].length, 
                                lon: data[0]["coords"]['lon'].reduce(reducer)/data[0]["coords"]['lon'].length
                            },
                    zoom: 13 
                    },
            margin: { r: 0, t: 0, b: 0, l: 0 }
        };
        
        Plotly.newPlot("divmap", alldata, layout);
    })
    .catch(error => {
        console.log(error)
    })
}

function getTables(data) {
    let tables =
        `<table id="tab1">
        <thead>
        <tr>
          <th>Sklep</th>
          <th>Zapotrzebowanie</th>
        </tr>
        </thead>
        <tbody>`
    for (let i = 0; i < data['input_data']['shops_nr']; i++) {
        tables += 
        `<tr>
            <td>` + data['input_data']['shops'][i] + `</td>
            <td>` + data['input_data']['shops_needs'][i] + `</td>
        </tr>`
    }
    tables += `</tbody></table>`

    tables += 
        `<table id="tab2">
        <thead>
        <tr>
          <th>Magazyn</th>
          <th>Ładunek</th>
        </tr>
        </thead>
        <tbody>`
    for (let i = 0; i < data['input_data']['warehouses_nr']; i++) {
        tables += 
        `<tr>
            <td>` + data['input_data']['warehouses'][i] + `</td> 
            <td>` + data['input_data']['warehouses_loads'][i] + `</td>
        </tr>`
    }
    tables += `</tbody></table>`

    return tables
}