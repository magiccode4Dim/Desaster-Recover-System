// Função para obter o valor de um cookie
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}


/** Busca valores na API */
var cookies = document.cookie.split(';');
var p, ip, id, nodes;

// Iterar pelos cookies e encontrar os valores de p, ip e id
for (var i = 0; i < cookies.length; i++) {
  var cookie = cookies[i].trim();
  if (cookie.startsWith('protocol=')) {
    p = cookie.substring('protocol='.length);
  } else if (cookie.startsWith('apiurl=')) {
    ip = cookie.substring('apiurl='.length);
  }
}

var nodesCookie = getCookie('nodes').substring(1, getCookie('nodes').length - 1);
; // Obtém o valor do cookie 'nodes'
nodes = nodesCookie.split("\\054")

// Função para fazer a requisição GET na API e atualizar o gráfico





/**Busca valores na API */

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

/*getDayWiseTimeSeries(new Date().getTime(), 10, {
  min: 10,
  max: 90
})*/

function getNewSeries(baseval, yrange) {
  var newDate = baseval + TICKINTERVAL;
  lastDate = newDate

  for (var i = 0; i < data.length - 10; i++) {
    data[i].x = newDate - XAXISRANGE - TICKINTERVAL
    data[i].y = 0
  }
  var upplusdown = 0;

  if (document.visibilityState === 'visible') {

    for (var i = 0; i < nodes.length; i++) {
      var apiUrl = `${p}://${ip}/api/statusservice/getlaststatus?id=${nodes[i]}`;
      fetch(apiUrl)
        .then(response => response.json())
        .then(apiData => {
          try {
            upplusdown += (apiData.totalup) + (apiData.totaldown);
          } catch (error) {
            console.error('Erro ao processar dados:', error);
          }
        })
        .catch(error => {
          console.error('Erro ao obter os dados da API:', error);
        });
    }

    // Após todas as requisições serem concluídas
    setTimeout(function () {
      var newDataPoint = {
        x: newDate,
        y: upplusdown
      };

      data.push(newDataPoint);

      if (data.length > XAXISRANGE / TICKINTERVAL) {
        data.shift();
      }

      chart.updateSeries([{ data }]);
    }, 1000); // Aguarda um tempo adequado para que todas as requisições sejam concluídas
  }



}

function resetData() {
  // Alternatively, you can also reset the data at certain intervals to prevent creating a huge series 
  data = data.slice(data.length - 10, data.length);
}



var options = {
  tooltip: {
    enabled: false, // Desabilita os tooltips
  },
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
    text: 'Utilização de Rede no Cluster (UPLOAD+DOWNLOAD)',
    align: 'left'
  },
  markers: {
    size: 0
  },
  xaxis: {
    type: 'datetime',
    range: XAXISRANGE,
    labels: {
      show: false,  // Oculta os rótulos do eixo x
    },
    title: {
      text: `Actualização dos ultimos ${nodes.length} segundos`, // Define o rótulo do eixo Y como "MB/s"
      style: {
        fontSize: '12px',
        fontWeight: 'bold',
      },
    },
  },
  yaxis: {
    //max: 1000,
    labels: {
      formatter: function (value) {
        return Math.round(value); // Arredonda para o valor inteiro mais próximo
      }
    },
    title: {
      text: 'MB', // Define o rótulo do eixo Y como "MB/s"
      style: {
        fontSize: '14px',
        fontWeight: 'bold',
      },
    },
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
}, nodes.length * 1000)