// selectors
var slider = document.getElementById("inputslider"); 
var dateControl = document.querySelector('input[type="date"]');
var imgSrc = document.getElementById("map");

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

// updates slider value and image when user enters an input
dateControl.onchange = function () {
  slider.value = newDaysOfYear.indexOf(dateControl.value);
  var xhr = new XMLHttpRequest();
  var imgName = "../imgs/cloudstest/" + dateControl.value + ".png";
  xhr.onreadystatechange = function () {
    if(this.readyState == 4 && this.status == 200){
      imgSrc.src = this.responseURL;
    }
  };
  xhr.open("GET", imgName, true);
  xhr.send();
}

// forces the default image to today's image
function defaultImage() {
  var xhr = new XMLHttpRequest();
  var imgName = "../imgs/cloudstest/" + dateControl.value + ".png";
  xhr.onreadystatechange = function () {
    if(this.readyState == 4 && this.status == 200){
      imgSrc.src = this.responseURL;
    }
  };
  xhr.open("GET", imgName, true);
  xhr.send();
}
defaultImage();

// on slider input adjust the image and the date input
slider.oninput = function () {
  var xhr = new XMLHttpRequest();
  var inputValues = this.value;
  dateControl.value = newDaysOfYear[inputValues];
  var imgName = "../imgs/cloudstest/" + dateControl.value + ".png";
  xhr.onreadystatechange = function () {
    if(this.readyState == 4 && this.status == 200){
      imgSrc.src = this.responseURL;
    }
  };
  xhr.open("GET", imgName, true);
  xhr.send();
  console.log(imgName);
}