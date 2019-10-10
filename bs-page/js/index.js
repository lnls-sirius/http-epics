
window.onload = function () {
    function monitor(pv, id){ 
        var previous_response_length = 0
        xhr = new XMLHttpRequest()
        xhr.open("GET", "http://10.0.38.42:7379/SUBSCRIBE/" + encodeURI(pv), true);

        var pv = {
            name:document.getElementById(name),
            value:document.getElementById(id),
        }
        pv.name.innerText = name;

        function checkData() {
            if(xhr.readyState == 3)  {
                response = xhr.responseText;
                chunk = response.slice(previous_response_length);
                previous_response_length = response.length;
                res = JSON.parse(JSON.parse(chunk).SUBSCRIBE[2])
                pv.value.innerText = res['value'];
            }
        };
        xhr.onreadystatechange = checkData;
        xhr.send(null);
    }

    monitor('BO-Fam:PS-B-2:Current-Mon', 'BO-Fam:PS-B-2:Current-Mon_value')
}

