

// chart = new Chart("myChart", {
//   type: "line",
//   data: {
//     labels: xValues,
//     datasets: [{
//       fill: false,
//       lineTension: 0,
//       backgroundColor: "rgba(0,0,255,1.0)",
//       borderColor: "rgba(0,0,255,0.1)",
//       data: yValues
//     }]
//   },
//   data: {
//     labels: xValues,
//     datasets: [{
//       fill: false,
//       lineTension: 0,
//       backgroundColor: "rgba(0,255,0,1.0)",
//       borderColor: "rgba(0,0,255,0.1)",
//       data: yValues
//     }]
//   },
//   options: {
//     legend: {display: false},
//     scales: {
//       yAxes: [{ticks: {min: 45, max:200}}],
//     }
//   }
// });

chart = new Chart("myChart", {
type: "line",
data: {
    labels: xValues,
    datasets: [{
    data: yValues,
    borderColor: "blue",
    fill: false
    },{
    data: yValues,
    borderColor: "blue",
    fill: false
    }]
},
options: {
    legend: {display: false},
    backdropColor: "black"
}
});

var barXValues = ["Italy", "France", "Spain", "USA", "Argentina"];
var barYValues = [55, 49, 44, 24, 15];
var barColors = ["red", "green","blue","orange","brown"];

barChart = new Chart("myBarChart", {
    type: "bar",
    data: {
      labels: barXValues,
      datasets: [{
        backgroundColor: barColors,
        data: barYValues
      }]
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: "Bar chart"
      }
    }
  });


function sendHeartRate(){
    sendHRT(randomRange(50,150));
}



const sendHRT = async (heartData) => {
    const url = '/getHeartRate'; // the URL to send the HTTP request to
    const body = JSON.stringify(heartData); // whatever you want to send in the body of the HTTP request
    const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
    const method = 'POST';
    const response = await fetch(url, { method, body, headers });
    const data = await response.text(); // or response.json() if your server returns JSON
}

const requestUpdates = async () => {
    const url = '/requestUpdate'; // the URL to send the HTTP request to
    const body = JSON.stringify(); // whatever you want to send in the body of the HTTP request
    const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
    const method = 'POST';
    const response = await fetch(url, { method, body, headers });
    const data = await response.text(); // or response.json() if your server returns JSON
    chart.data.datasets[0].data = []
    chart.data.datasets[1].data = []
    // chart.data.datasets.forEach((dataset) => {
    //     dataset.data.forEach((element) => {
    //         dataset.data.pop();
    //     })
    // });
    console.log(chart.data.datasets[0].data)
    array = removeChar(data).slice(0, -1).split(",")
    console.log(array)
    var total = 0;

    for ( let i = 0; i < array.length; i++ ) {
        total += parseInt(array[i]);
    }
    average = total / array.length
    console.log(average)

    for (var i = 0; i < 50; i++) {
        chart.data.datasets[0].data.push(parseInt(array[i]))
    }
    for (var i = 0; i < 50; i++){
        chart.data.datasets[1].data.push(average)
    }

    if (array[array.length-1] > average){
        chart.data.datasets[0].borderColor = "red"
    } else {
        chart.data.datasets[0].borderColor = "green"
    }

    // console.log(chart.data.datasets[0].data)
    chart.update()
    
}

function randomRange(min, max) {

	return Math.floor(Math.random() * (max - min + 1)) + min;

}


const removeChar = (str) => str.slice(1, -1);

async function test(){
    while (true) {
        requestUpdates()
        await sleep(1000)
    }
}

const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}


test();