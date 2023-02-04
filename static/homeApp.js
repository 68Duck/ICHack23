xInput = document.getElementById("xInput")
yInput = document.getElementById("yInput")
fileInput = document.getElementById("fileInput")
test = document.getElementById("test")


function goToDot(){
    sendDot([xInput.value, yInput.value])
}

function printFile(){
    console.log(fileInput.value)
    test.innerHTML = "<iframe src='" + fileInput.value + "' width='100%' height='600px' frameborder='0'></iframe>"
}


const sendDot = async (dotData) => {
    const url = '/sendDot'; // the URL to send the HTTP request to
    const body = JSON.stringify(dotData); // whatever you want to send in the body of the HTTP request
    const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
    const method = 'POST';
    const response = await fetch(url, { method, body, headers });
    const data = await response.text(); // or response.json() if your server returns JSON
}