// selectors
var slider = document.getElementById("inputslider"); 
var dateControl = document.querySelector('input[type="date"]');

// loops through the dates backwards
var d = new Date();
var daysOfYear = [];
for (i = 0; i <= 100; i++) {
  var b = d.setDate(d.getDate() - 1);
  daysOfYear.push(new Date(b).toJSON());
}

// converts daysOfYear to the correct date format
var newDaysOfYear = [];
for (j = 0; j <= 100; j++){
  var c = daysOfYear[j].replace(/T.*/, "");
  newDaysOfYear.push(c);
}

dateControl.value = newDaysOfYear[0]; //default value onload

// iterates oninput inputValues over daysOfYear array
slider.oninput = function () {
  var inputValues = this.value;
  dateControl.value = newDaysOfYear[inputValues];
}

// updates slider value when user enters an input
dateControl.onchange = function () {
  var getValue = document.getElementById("date").value;
  slider.value = newDaysOfYear.indexOf(getValue);
}

