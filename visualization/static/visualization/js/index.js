window.onload = function() { 
    var doc = document.getElementById('div1')
    doc.innerHTML += '{{ test }}'
}

fetch('visualization/result', {
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
})
.catch(error => {
    console.log(error)
})