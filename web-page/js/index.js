
window.onload = function () {
    var previous_response_length = 0
    xhr = new XMLHttpRequest()
    xhr.open("GET", "http://0.0.0.0:7379/SUBSCRIBE/" + encodeURI('MTEST:RAND'), true);

    var pv1 = {
        name:document.getElementById("n1"),
        severity:document.getElementById("s1"),
        timestamp:document.getElementById("t1"),
        value:document.getElementById("v1"),
        unit:document.getElementById("u1"),
        host:document.getElementById("h1"),
    }
    pv1.name.innerText = 'MTEST:RAND'

    function checkData() {
        if(xhr.readyState == 3)  {
            response = xhr.responseText;
            chunk = response.slice(previous_response_length);
            previous_response_length = response.length;
            res = JSON.parse(JSON.parse(chunk).SUBSCRIBE[2]);
            pv1.severity.innerText = res['severity'];
            pv1.timestamp.innerText = res['timestamp'];
            pv1.value.innerText = res['value'];
            pv1.unit.innerText = res['unit'];
            pv1.host.innerText = res['host'];
        }
    };

    xhr.onreadystatechange = checkData;
    xhr.send(null);
}

