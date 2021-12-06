
   
'use strict';

// PLANT CONDITION LINE GRAPH
let user_plant_info = document.getElementById('users_plants_id').value 

$.get(`/conditiondata/${user_plant_info}`, res => {

    const conditions = {'healthy': 4, 'brown leaves': 3, 'black spots': 2, 'wilting': 1, 'dying': 0} 
    const conditions_reverse = {4:'healthy', 3:'brown leaves', 2:'black spots', 1:'wilting', 0:'dying'}
    const data = [];
        for (const dailyCondition of res.data) {
        // show conditions on y axis
        data.push({x: dailyCondition.date, y: conditions[dailyCondition.plant_condition]});
  }
  
    new Chart($('#conditionChart'), {
      type: 'line',
      data: {
        datasets: [
          {
            label: 'Plant Condition',
            data,  // equivalent to data: data
            backgroundColor: "#6E8B3D",
            borderColor: "#6E8B3D",
            borderDash: [5,5]
          },
        ],
      },
      options: {
        scales: {
          x: {
            type: 'time',
            time: {
              // Luxon format string
              tooltipFormat: 'LLLL dd',
              unit: 'day',
            },
          },
          y: {
            ticks: {
              backgroundColor: "#6E8B3D",
              callback: function(label, index, labels) {
                if (label in conditions_reverse) {
                  return conditions_reverse[label];
                }
                else {
                  return " ";
                }
              }
            }
          }
        },
      },
    });
  });