
// Obter os cookies da requisição
var cookies = document.cookie.split(';');
var p, ip, id;

// Iterar pelos cookies e encontrar os valores de p, ip e id
for (var i = 0; i < cookies.length; i++) {
  var cookie = cookies[i].trim();
  if (cookie.startsWith('protocol=')) {
    p = cookie.substring('protocol='.length);
  } else if (cookie.startsWith('apiurl=')) {
    ip = cookie.substring('apiurl='.length);
  } else if (cookie.startsWith('serverID=')) {
    id = cookie.substring('serverID='.length);
  }
}

// Função para fazer a requisição GET na API e atualizar o gráfico
function atualizarGrafico() {
    var apiUrl = `${p}://${ip}/api/statusservice/getlaststatus?id=${id}`;
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // Aqui, data deve ser um objeto JSON contendo os dados da série de acordo com a estrutura esperada

            // Supondo que os dados estejam em um objeto JSON com as chaves cpu, memoria e armazenamento
            var cpuValue = data.cpu;
            var memoriaValue = data.memory;
            var armazenamentoValue = data.disc;

            // Atualize a série de dados com os valores recebidos da API
            chart.updateSeries([cpuValue, memoriaValue, armazenamentoValue]);
        })
        .catch(error => {
            console.error('Erro ao obter os dados da API:', error);
        });
}



var initialSeries = [0, 0, 0];

var options = {
    series: initialSeries,
    chart: {
        height: 390,
        type: 'radialBar',
    },
    plotOptions: {
        radialBar: {
            offsetY: 0,
            startAngle: 0,
            endAngle: 270,
            hollow: {
                margin: 5,
                size: '30%',
                background: 'transparent',
                image: undefined,
            },
            dataLabels: {
                name: {
                    show: false,
                },
                value: {
                    show: false,
                }
            }
        }
    },
    colors: ['#1ab7ea', '#0084ff', '#39539E'],
    labels: ['CPU', 'RAM', 'STORAGE'],
    legend: {
        show: true,
        floating: true,
        fontSize: '16px',
        position: 'left',
        offsetX: 160,
        offsetY: 15,
        labels: {
            useSeriesColors: true,
        },
        markers: {
            size: 0
        },
        formatter: function (seriesName, opts) {
            return seriesName + ":  " + opts.w.globals.series[opts.seriesIndex]
        },
        itemMargin: {
            vertical: 3
        }
    },
    responsive: [{
        breakpoint: 480,
        options: {
            legend: {
                show: false
            }
        }
    }]
};

var chart = new ApexCharts(document.querySelector("#serverchart"), options);
chart.render();

function atualizarGraficoPeriodicamente() {
    function atualizarSeVisivel() {
      if (document.visibilityState === 'visible') {
        atualizarGrafico();
      }
    }
  
    setInterval(atualizarSeVisivel, 1000); // 1000 milissegundos = 1 segundo
  }
// Chame a função para atualizar o gráfico inicialmente
atualizarGrafico();

// Chame a função para atualizar o gráfico a cada 1 segundo
atualizarGraficoPeriodicamente();