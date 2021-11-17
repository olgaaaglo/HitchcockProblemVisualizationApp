// d3.csv(
// 	"https://raw.githubusercontent.com/plotly/datasets/master/2015_06_30_precipitation.csv",
// 	function(err, rows) {
// 		function unpack(rows, key) {
// 			return rows.map(function(row) {
// 				return row[key];
// 			});
// 		}

// 		var data = [
// 			{
// 				type: "scattermapbox",
// 				lon: unpack(rows, "Lon"),
// 				lat: unpack(rows, "Lat"),
// 				marker: { color: "fuchsia", size: 4 }
// 			}
// 		];

// 		var layout = {
//             autosize: false,
//             width: 500,
//             height: 500,
// 			dragmode: "zoom",
// 			mapbox: { style: "open-street-map", center: { lat: 38, lon: -90 }, zoom: 3 },
// 			margin: { r: 0, t: 0, b: 0, l: 0 }
// 		};

// 		Plotly.newPlot("div1", data, layout);
// 	}
// );


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
    alldata = []
    data = data["coords"]
    
    //for (var i; i < data.length; i++)
    //{
        var mapdata = [
            {
                type: "scattermapbox",
                lon: data[0]['lon'],
                lat: data[0]['lat'],
                marker: { color: "fuchsia", size: 4 },
                mode: "lines"
            }
        ];

        alldata.push(mapdata)
    //}

    var reducer = (a, b) => (a + b)
        
    var layout = {
        autosize: false,
        width: 500,
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

    Plotly.newPlot("div1", mapdata, layout);
})
.catch(error => {
    console.log(error)
})