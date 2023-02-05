updateBarValues()

var barYValues = [0, 0, 0, 0, 0]
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
    // console.log(chart.data.datasets[0].data)
    array = removeChar(data).slice(0, -1).split(",")
    // console.log(array)
    var total = 0;

    for ( let i = 0; i < array.length; i++ ) {
        total += parseInt(array[i]);
    }
    average = total / array.length
    // console.log(average)

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

    for (var i = 0; i < 50; i++) {
        yValues[i] = array[i]
    }


    barYValues = updateBarValues()

    barChart.data.datasets[0].data = []
    for (var i = 0; i < 5; i++){
        barChart.data.datasets[0].data.push(barYValues[i])
    }
    console.log(barYValues)
    barChart.update()
    
}

function drawSVG(){
    var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height"),
    r = Math.min(width, height) / 2,
    g = svg
            .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    
    // Define the data to plot
    var dataDicts = [];
    for (var i = 0; i < 40, i++;) {
    dataDicts.push({"angle": (i + 1) * 9, "value": 60})
    }
    var newData;
    for (var counter = 0; counter++;) {
      // Scale the data values to a radial axis
      var angle = d3.scaleLinear()
              .domain([0, 360])
              .range([0, 2 * Math.PI]);
      var radius = d3.scaleLinear()
              .domain([0, 100])
              .range([0, r]);

      // Define the line generator
      var line = d3.lineRadial()
              .angle(function (d) {
                return angle(d.angle);
              })
              .radius(function (d) {
                return radius(d.value);
              });

      // Plot the data
      g.append("path")
              .datum(data)
              .attr("d", line)
              .attr("fill", "none")
              .attr("stroke", "blue");
      newData = data[data.length - 1]
      data[counter % 15]["value"] = newData
    }
  }

drawSVG()



function updateBarValues(){
    var barYValues = [0, 0, 0, 0, 0]
    for (var i = 0; i < yValues.length; i++){
        console.log("test")
        var value = yValues[i]
        console.log(value)
        if (value < 80){
            barYValues[0] = barYValues[0] + 1
        } else if (value < 100) {
            barYValues[1] = barYValues[1] + 1
        } else if (value < 120) {
            barYValues[2] = barYValues[2] + 1
        } else if (value < 160) {
            barYValues[3] = barYValues[3] + 1
        } else {
            barYValues[4] = barYValues[4] + 1
        }
    }
    console.log(barYValues)
    return barYValues
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