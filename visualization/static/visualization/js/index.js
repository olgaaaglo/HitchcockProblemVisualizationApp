// window.onload = function() { 
//     var doc = document.getElementById('div1')
//     doc.innerHTML += '{{ test }}'
// }

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


fetch(url, {//'visualization/result', {
    method: 'GET',
    headers:{
        'Content-Type': 'application/json',
        //'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
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
    //Perform actions with the response data from the view
    console.log(data);
    var data = [
        {
            type: "scattermapbox",
            lon: data['lon'],
            lat: data['lat'],
            marker: { color: "fuchsia", size: 4 },
            mode: "lines"
        }
    ];

    var layout = {
        autosize: false,
        width: 500,
        height: 500,
        dragmode: "zoom",
        mapbox: { style: "open-street-map", center: { lat: 33.7742915, lon: -84.4023762 }, zoom: 13 },
        margin: { r: 0, t: 0, b: 0, l: 0 }
    };

    Plotly.newPlot("div1", data, layout);
})
.catch(error => {
    console.log(error)
})