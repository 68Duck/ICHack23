var x = 0
var y = 0
const dot = document.getElementById("dot")

const requestUpdates = async () => {
    const url = '/requestUpdate'; // the URL to send the HTTP request to
    const body = JSON.stringify(); // whatever you want to send in the body of the HTTP request
    const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
    const method = 'POST';
    const response = await fetch(url, { method, body, headers });
    const data = await response.text(); // or response.json() if your server returns JSON
    console.log(data)
    coordinate = data.split(",")
    console.log(coordinate[0])
    console.log(coordinate[1])
    dot.style.setProperty("--left", x)
    dot.style.setProperty("--top", y)
}

async function test(){
    while (true) {
        requestUpdates()
        await sleep(200)
    }
}



const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

test();