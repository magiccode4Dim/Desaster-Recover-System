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
 // Obtém o valor do cookie 'nodes'
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

async function getNewSeries(baseval, yrange) {
  var newDate = baseval + TICKINTERVAL;
  lastDate = newDate;

  for (var i = 0; i < data.length - 10; i++) {
    data[i].x = newDate - XAXISRANGE - TICKINTERVAL;
    data[i].y = 0;
  }

  var upplusdown = 0;
  var ramusagenodes = new Array();
  var storagenodes = new Array();
  var cpuvaluesnodes = 0;
  if (document.visibilityState === 'visible') {
    try {
      const fetchPromises = nodes.map(async (node, index) => {
        const apiUrl = `${p}://${ip}/api/statusservice/getlaststatus?id=${node}`;
        const response = await fetch(apiUrl);
        const apiData = await response.json();
        console.log("Depois ", index);
        
        upplusdown += apiData.totalup + apiData.totaldown;
        cpuvaluesnodes += apiData.cpu;

        ramusagenodes[index] = apiData.memory;
        storagenodes[index] = apiData.disc;
      });

      await Promise.all(fetchPromises);

      var newDataPoint = {
        x: newDate,
        y: upplusdown
      };

      data.push(newDataPoint);

      if (data.length > XAXISRANGE / TICKINTERVAL) {
        data.shift();
      }
      
      console.log(ramusagenodes);
      chart.updateSeries([{ data }]);
      chart2.updateSeries([{ data: ramusagenodes }]);
      chart3.updateSeries([cpuvaluesnodes / nodes.length]);
      chart4.updateSeries([{ data: storagenodes }]);
    } catch (error) {
      console.error('Erro ao processar dados:', error);
    }
  }
}


function resetData() {
  // Alternatively, you can also reset the data at certain intervals to prevent creating a huge series 
  data = data.slice(data.length - 10, data.length);
}


//Bandusage chart begginnnn

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


//Bandusage chart end

//memoryusage chart  begginnn

var options = {
  series: [{
  data: [],
  name: 'RAM',
}],
  chart: {
  type: 'bar',
  height: 350
},
plotOptions: {
  bar: {
    borderRadius: 4,
    horizontal: true,
  }
},
title: {
  text: 'Utilização de Memoria RAM',
  align: 'left'
},
dataLabels: {
  enabled: false
},
xaxis: {
  categories: nodes,
  title: {
    text: "Percentagem (%)", // Define o rótulo do eixo Y como "MB/s"
    style: {
      fontSize: '12px',
      fontWeight: 'bold',
    }}
  
}
};

var chart2 = new ApexCharts(document.querySelector("#memorychart"), options);
chart2.render();

//memory usage chart end

//cpu media usage chart begginnn
var options = {
  series: [0],
  chart: {
  height: 350,
  type: 'radialBar',
  offsetY: -10
},
plotOptions: {
  radialBar: {
    startAngle: -135,
    endAngle: 135,
    dataLabels: {
      name: {
        fontSize: '16px',
        color: undefined,
        offsetY: 120
      },
      value: {
        offsetY: 76,
        fontSize: '22px',
        color: undefined,
        formatter: function (val) {
          return val + "%";
        }
      }
    }
  }
},
fill: {
  type: 'gradient',
  gradient: {
      shade: 'dark',
      shadeIntensity: 0.15,
      inverseColors: false,
      opacityFrom: 1,
      opacityTo: 1,
      stops: [0, 50, 65, 91]
  },
},
stroke: {
  dashArray: 4
},
labels: ['Media de utilização da CPU no Cluster'],
};

var chart3 = new ApexCharts(document.querySelector("#mediacpuusage"), options);
chart3.render();


//cpu media usage chart end


//storage chart begginnn

var options = {
  series: [{
  name: 'DISC',
  data: []
}],
  chart: {
  height: 350,
  type: 'bar',
},
plotOptions: {
  bar: {
    borderRadius: 10,
    dataLabels: {
      position: 'top', // top, center, bottom
    },
  }
},
dataLabels: {
  enabled: true,
  formatter: function (val) {
    return val + "%";
  },
  offsetY: -20,
  style: {
    fontSize: '12px',
    colors: ["#304758"]
  }
},

xaxis: {
  categories: nodes,
  position: 'top',
  axisBorder: {
    show: false
  },
  axisTicks: {
    show: false
  },
  crosshairs: {
    fill: {
      type: 'gradient',
      gradient: {
        colorFrom: '#D8E3F0',
        colorTo: '#BED1E6',
        stops: [0, 100],
        opacityFrom: 0.4,
        opacityTo: 0.5,
      }
    }
  },
  tooltip: {
    enabled: true,
  }
},
yaxis: {
  axisBorder: {
    show: false
  },
  axisTicks: {
    show: false,
  },
  labels: {
    show: false,
  }

},
title: {
  text: 'Utilização do Armazenamento no Cluster (%)',
  floating: true,
  offsetY: 330,
  align: 'center',
  style: {
    color: '#444'
  }
}
};

var chart4 = new ApexCharts(document.querySelector("#storagechart"), options);
chart4.render();
//storage chart end