$(document).ready(function () {
    var ctx = document.getElementById('vote_chart').getContext('2d');
    var vote_chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [''],
            datasets: [{
                label: '',
                data: [0],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
});