
   
'use strict';
let user_plant_info = document.getElementById('users_plants_id').value 
console.log(user_plant_info)
$.get('/conditiondata', (res) => {
    let ConditionData = res;

    let condition = document.getElementById('conditonChart');
    let conditionChart = new Chart(condition, {
        type: 'bar',
        data: {
            labels: ["healthy", "brown leaves", "black spots", "wilting", "dying"],
            datasets: [
                {
                    backgroundColor: [],
                    data: ConditionData
                }
            ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            legend: { display: false },
            title: {
                display: true,
                text: 'Weekly Condition Data'
            },
        }
    });
});

