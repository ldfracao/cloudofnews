var slider = document.getElementById("inputslider");
var date = document.getElementById("date");
var span = document.getElementById("span");
var sliderValue = document.getElementById("inputslider").getAttribute("value");

// loops through the dates backwards
var d = new Date();
var daysOfYear = [];
for (i = 0; i < 100; i++) {
  daysOfYear[0] = new Date();
  var b = d.setDate(d.getDate() - 1);
  daysOfYear.push(new Date(b));
}

date.innerHTML = daysOfYear[0]; // default date onload

// iterates inputValues over daysOfYear array
slider.oninput = function () {
  var inputValues = this.value;
  date.innerHTML = daysOfYear[inputValues];
}


