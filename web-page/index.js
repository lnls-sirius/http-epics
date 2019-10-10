
window.onload = function () {
    var previous_response_length = 0
    xhr = new XMLHttpRequest()
    xhr.open("GET", "http://10.0.6.48:7379/SUBSCRIBE/" + encodeURI('MTEST:RAND'), true);

    var val = document.getElementById("val");

    function checkData() {
        if(xhr.readyState == 3)  {
            response = xhr.responseText;
            chunk = response.slice(previous_response_length);
            previous_response_length = response.length;
            res = JSON.parse(JSON.parse(chunk).SUBSCRIBE[2]);
            val.innerText = res['value'];
        }
    };

    xhr.onreadystatechange = checkData;
    xhr.send(null);
}

