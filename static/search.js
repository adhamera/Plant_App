const search_plants = ["Zebra Plant", "Jade Plant", "Crown of Thorns", "Weeping Fig", "Sago Palm", "Golden Pothos", "Snake Plant", "Wax Plant Begonia", "Umbrella Plant", "Arrowhead Plant"]
const linkList = []
function givePlantLinks(plant){
    return search_plants.indexOf(plant) + 1
}

 
function searchAutocomplete(input) {
    let formattedInput = input.toLowerCase()
    if (formattedInput == '') {
    return [];
    }
    let reg = new RegExp(formattedInput)
    return search_plants.filter(function(plant) {
        if (plant.toLowerCase().match(reg)) {
        return plant;
        }
    });
}
 
function showPlantResults(value) {
  result = document.getElementById("result");
  result.innerHTML = '';
  let list = '';
  let terms = searchAutocomplete(value);
  for (i=0; i<terms.length; i++) {
    list += '<li>' + `<a href="/plants/${givePlantLinks(terms[i])}">` + terms[i] + '</a>' + '</li>';
  }
  result.innerHTML = '<ul>' + list + '</ul>';
}