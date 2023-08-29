

/** Busca valores na API 
var cookies = document.cookie.split(';');
var p, ip, id;

// Iterar pelos cookies e encontrar os valores de p, ip e id
for (var i = 0; i < cookies.length; i++) {
  var cookie = cookies[i].trim();
  if (cookie.startsWith('protocol=')) {
    p = cookie.substring('protocol='.length);
  } else if (cookie.startsWith('apiurl=')) {
    ip = cookie.substring('apiurl='.length);
  }
}

// Função para fazer a requisição GET na API e atualizar o gráfico





/**Busca valores na API 

var options = {
  series: [{
    data: [10, 20, 30, 40, 50]
  }],
  chart: {
    id: 'realtime',
    height: 350,
    type: 'line',
    animations: {
      enabled: true,
      easing: 'linear',
      dynamicAnimation: {
        speed: 1000
      }
    },
    toolbar: {
      show: false
    },
    zoom: {
      enabled: false
    }
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth'
  },
  title: {
    text: 'Dynamic Updating Chart',
    align: 'left'
  },
  markers: {
    size: 0
  },
  xaxis: {
    type: 'datetime',
    range: XAXISRANGE,
  },
  yaxis: {
    max: 100
  },
  legend: {
    show: false
  },
};

var chart = new ApexCharts(document.querySelector("#bandchart"), options);
chart.render();


window.setInterval(function () {
  getNewSeries(lastDate, {
    min: 10,
    max: 90
  })
  var apiUrl = `${p}://${ip}/api/statusservice/getlaststatus?id=MASTER`;
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // Aqui, data deve ser um objeto JSON contendo os dados da série de acordo com a estrutura esperada

            // Supondo que os dados estejam em um objeto JSON com as chaves cpu, memoria e armazenamento
            var cpuValue = data.memory;

            chart.updateSeries([{
              data: [10, 20, 30, 40, 50]
            }])

        })
        .catch(error => {
            console.error('Erro ao obter os dados da API:', error);
        });

  
}, 1000)
*/

var lastDate = 0;
var data = []
var TICKINTERVAL = 86400000
let XAXISRANGE = 777600000
function getDayWiseTimeSeries(baseval, count, yrange) {
  var i = 0;
  while (i < count) {
    var x = baseval;
    var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

    data.push({
      x, y
    });
    lastDate = baseval
    baseval += TICKINTERVAL;
    i++;
  }
}

getDayWiseTimeSeries(new Date().getTime(), 10, {
  min: 10,
  max: 90
})

function getNewSeries(baseval, yrange) {
  var newDate = baseval + TICKINTERVAL;
  lastDate = newDate

  for (var i = 0; i < data.length - 10; i++) {
    // IMPORTANT
    // we reset the x and y of the data which is out of drawing area
    // to prevent memory leaks
    data[i].x = newDate - XAXISRANGE - TICKINTERVAL
    data[i].y = 0
  }

  data.push({
    x: newDate,
    y: Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min
  })
}

function resetData() {
  // Alternatively, you can also reset the data at certain intervals to prevent creating a huge series 
  data = data.slice(data.length - 10, data.length);
}



var options = {
  series: [{
    data: data.slice()
  }],
  chart: {
    id: 'realtime',
    height: 350,
    type: 'line',
    animations: {
      enabled: true,
      easing: 'linear',
      dynamicAnimation: {
        speed: 1000
      }
    },
    toolbar: {
      show: false
    },
    zoom: {
      enabled: false
    }
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth'
  },
  title: {
    text: 'Dynamic Updating Chart',
    align: 'left'
  },
  markers: {
    size: 0
  },
  xaxis: {
    type: 'datetime',
    range: XAXISRANGE,
  },
  yaxis: {
    max: 100
  },
  legend: {
    show: false
  },
};

var chart = new ApexCharts(document.querySelector("#bandchart"), options);
chart.render();


window.setInterval(function () {
  getNewSeries(lastDate, {
    min: 10,
    max: 90
  })

  chart.updateSeries([{
    data: data
  }])
}, 1000)