function matches_donut_chartsjs(matches) {
    for (var i = 0; i < matches.length; i++) {
        generateDonutChartJs('chartjs-' + matches[i].id, matches[i].chartjs_data, matches[i].chartjs_labels, matches[i].match_name)
    }
}

function generateDonutChartJs(id, data, labels, match_title) {
    var ctx = document.getElementById(id).getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: match_title,
                data: data,
                backgroundColor: [
                    'rgba(255, 217, 6, .3)',
                    'rgba(0, 175, 80, .3)',
                    'rgba(11, 103, 216, .3)',
                    'rgba(14, 31, 123, .3)',
                    'rgba(208, 3, 3, .3)',
                    'rgba(134, 134, 134, .3)'
                ],
                borderColor: [
                    'rgb(255, 217, 6)',
                    'rgb(0, 175, 80)',
                    'rgb(11, 103, 216)',
                    'rgb(14, 31, 123)',
                    'rgb(208, 3, 3)',
                    'rgb(134, 134, 134)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            legend: {                // http://www.chartjs.org/docs/latest/configuration/legend.html
                display: true,
                position: 'bottom',
                labels: {
                    fontColor: '#fff',
                    boxWidth: 12
                }
            },
            pieceLabel: {            // https://github.com/emn178/Chart.PieceLabel.js
                render: 'percentage',
                fontSize: 12,
                fontStyle: 'bold',
                fontFamily: '"Source Sans Pro", sans-serif',
                fontColor: '#fff',
                // fontColor: function (data) {
                //     var rgb = data.dataset.backgroundColor[data.index];
                // //  var rgb = hexToRgb(data.dataset.backgroundColor[data.index]);
                //     var threshold = 140;
                //     var luminance = 0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b;
                //     return luminance > threshold ? 'black' : 'white';
                // },
                arc: true,
                position: 'border',
                precision: 2
            },
            title: {                  // http://www.chartjs.org/docs/latest/configuration/title.html
                display: true,
                text: match_title,
                fontColor: '#cdcdcd',
                fontSize: 14,
                fontFamily: '"Source Sans Pro", sans-serif'
            },
            animation: {
                animateScale: true,
                animateRotate: true
                //easing: 'easeOutBounce'
            },
            layout: {
                padding: {
                    left: 0,
                    right: 0,
                    top: 0,
                    bottom: 0
                }
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        var dataset = data.datasets[tooltipItem.datasetIndex];
                        var total = dataset.data.reduce(function (previousValue, currentValue, currentIndex, array) {
                            return previousValue + currentValue;
                        });
                        var precentage = (dataset.data[tooltipItem.index] * 100) / total;
                        return data.labels[tooltipItem.index] + ' - ' + precentage.toFixed(2) + '%';
                    }
                }
            }
        }
    });
}

