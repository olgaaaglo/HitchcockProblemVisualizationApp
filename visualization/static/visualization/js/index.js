function visualize() {
    const city = document.getElementById("city").value;
    const shop = document.getElementById("shop").value;
    const warehouse = document.getElementById("warehouse").value;

    fetch('/visualization/find/' + city + '/' + shop + '/' + warehouse,{
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

        document.getElementById('divinfo').innerHTML = 
        `<p>Magazyny są zaznaczone kolorem czerwonym, a każdy sklep i trasy do niego tym samym innym od reszty kolorem.</p>`; //getInputTables(data);

        document.getElementById('change').innerHTML = 
        `<h3 class="header">Wyniki dla algorytmu symulowanego wyżarzania</h3>
        <form action="javascript:reDrawMap()" method="post">
            <input type="submit" value="Rysuj dla algorytmu transportowego" id="changeButton">
        </form>`;

        drawMap(data);

        document.getElementById('tables').innerHTML = getResultTables(data);
    })
    .catch(error => {
        console.log(error)
    })
}

function drawMap(data) {
    let alldata = [];
    data = data["results"];
    
    const colors = ["fuchsia", "blue", "green", "orange", "cyan", "purple", "black", "hotpink", "brown", "yellow"]
    const shops = data.map((element) => element["shop"]).filter((value, index, self) => self.indexOf(value) === index)

    for (let i = 0; i < data.length; i++)
    {
        if (data[i]["cargo"] != 0) {
            let shop_color = colors[shops.indexOf(data[i]["shop"]) % 10]

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
}

function reDrawMap() {
    let changeButton = document.getElementById('changeButton');
    let simulatedAnnealing = 1;

    let text = 'Wyniki dla algorytmu symulowanego wyżarzania';
    let buttonValue = 'Rysuj dla algorytmu transportowego';

    if (changeButton.value === "Rysuj dla algorytmu transportowego") {
        simulatedAnnealing = 0;
        text = 'Wyniki dla algorytmu transportowego';
        buttonValue = 'Rysuj dla algorytmu symulowanego wyżarzania'
    }

    fetch('/visualization/get_results_to_redraw/' + simulatedAnnealing,{
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
        document.getElementById('change').innerHTML = 
        `<h3 class="header">` + text + `</h3>
        <form action="javascript:reDrawMap()" method="post">
            <input type="submit" value="` + buttonValue + `" id="changeButton">
        </form>`

        drawMap(data);

        document.getElementById('tables').innerHTML = getResultTables(data);
    })
    .catch(error => {
        console.log(error)
    })
}

// function getInputTables(data) {
//     let tables =
//         `<table id="tab1">
//         <thead>
//         <tr>
//           <th>Sklep</th>
//           <th>Zapotrzebowanie</th>
//         </tr>
//         </thead>
//         <tbody>`
//     for (let i = 0; i < data['input_data']['shops'].length; i++) {
//         tables += 
//         `<tr>
//             <td>` + data['input_data']['shops'][i] + `</td>
//             <td>` + data['input_data']['shops_needs'][i] + `</td>
//         </tr>`
//     }
//     tables += `</tbody></table>`

//     tables += 
//         `<table id="tab2">
//         <thead>
//         <tr>
//           <th>Magazyn</th>
//           <th>Zasoby</th>
//         </tr>
//         </thead>
//         <tbody>`
//     for (let i = 0; i < data['input_data']['warehouses'].length; i++) {
//         tables += 
//         `<tr>
//             <td>` + data['input_data']['warehouses'][i] + `</td> 
//             <td>` + data['input_data']['warehouses_loads'][i] + `</td>
//         </tr>`
//     }
//     tables += `</tbody></table>`

//     return tables
// }

function getResultTables(data) {
    let input = data['input_data'];
    data = data["results"];

    let warehouse = data[0]['warehouse'];
    let shops_nr = data.filter((value) => value['warehouse'] === warehouse).length;

    let head = "";
    let body1 = "";
    let body2 = "";
    let last1 = `<tr><th scope="row" class="topBorder">Zapotrzebowanie </br> sklepów</th>`;
    let last2 = `<tr><th scope="row" class="topBorder">Suma</th>`;

    let rowSum = 0;
    let columnSum = new Array(shops_nr).fill(0);

    let warehouse_sum = 0;

    let sumaNadmiaruPodazy = 0;
    let sumaNadmiaruPopytu = 0;

    for (let i = 0; i < data.length; i++) {
        if (i < shops_nr) {
            head += `<th>` + data[i]["shop"] + `</th>`;

            let shop_need = input['shops_needs'][input['shops'].indexOf(data[i]["shop"])];
            last1 += `<td class="topBorder">` + shop_need + `</td>`;
            last2 += `<td class="topBorder">` + shop_need + `</td>`;

            columnSum[i % shops_nr] = parseInt(shop_need);
        }

        if (i % (shops_nr) == 0) {
            body1 += 
            `<tr>
            <th scope="row">` + data[i]['warehouse'] + `</th>`;
            body2 += 
            `<tr>
            <th scope="row">` + data[i]['warehouse'] + `</th>`;
        }
        
        body1 += 
            `<td>` + data[i]['length'] + `</td>`;
        if (data[i]['cargo'] != 0) {
            body2 += 
                `<td>` + data[i]['cargo'] + `</td>`;
            rowSum += parseInt(data[i]['cargo']);
            columnSum[i % shops_nr] -= parseInt(data[i]['cargo']);
        }
        else {
            body2 += 
                `<td></td>`;
        }
        
        if ((i + 1) % (shops_nr) == 0) {
            let warehouse_load = input['warehouses_loads'][input['warehouses'].indexOf(data[i]["warehouse"])];
            body1 += `<td class="leftBorder">` + warehouse_load + `</td></tr>`;

            body2 += `<td>` + (warehouse_load - rowSum != 0 ? warehouse_load - rowSum : "") + `</td>`;
            
            sumaNadmiaruPodazy += warehouse_load - rowSum;
            rowSum = 0;
            
            body2 += `<td class="leftBorder">` + warehouse_load + `</td></tr>`;

            warehouse_sum += warehouse_load;
        }
    }

    
    let overload = "";
    for (let i = 0; i < shops_nr; i++) {
        overload += `<td>` + (columnSum[i] != 0 ? columnSum[i] : "") + `</td>`;
        sumaNadmiaruPopytu += columnSum[i];
    }

    let tables =
        `</br><h4>Tabela kosztów (długości tras)</h4>
        <table>
        <thead>
        <tr> 
            <th rowspan="2">Magazyny</th>
            <th colspan=` + shops_nr + `>Sklepy</th> 
            <th rowspan="2" class="leftBorder">
                Zasoby </br>
                magazynów
            </th> 
        </tr> 
        <tr>` + head + `</tr>
        </thead>
        <tbody>` + 
            body1 + 
            last1 + `<td class="leftBorder topBorder"></td></tr></tbody>
        </table>
        
        <h4>Tabela ładunków</h4>
        <table>
        <thead>
        <tr>
            <th rowspan="2">Magazyny</th>
            <th colspan=` + (shops_nr + 1) + `>Sklepy</th> 
            <th rowspan="2" class="leftBorder">
                Suma
            </th> 
        </tr> 
        <tr>` + head + `<th class="rightBorder">Nadmiar podaży</th></tr>` +
        `</thead>
        <tbody>` + body2 + 
        `<tr><th>Nadmiar popytu</th>` + overload + `<td></td><td class="leftBorder">`
        + sumaNadmiaruPopytu + `</td></tr>` + last2 + 
        `<td class="topBorder">` + sumaNadmiaruPodazy + `</td>
        <td class="leftBorder topBorder">` + (warehouse_sum + sumaNadmiaruPopytu) + `</td>
        </tr>
        </tbody>
        </table>`;

    return tables;
}