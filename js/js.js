// document.getElementById("date").innerHTML = new Date();

//
// output.innerHTML = Date();

// loop through the date backwards
function dateloop() {
  var now = new Date();
  var daysOfYear = [];
  for (var d = new Date(); d <= now; d.setDate(d.getDate() - 1)) {
    daysOfYear.push(new Date(d));
  }
}
dateloop();
// decompose Date() into Date().getMonth...
// let year = Date().getFullYear();
// let month = Date().getMonth();
// let day = Date().getHours();

// console.log(typeof year);

// function dateloop() {
//   year -= 1;
//   month -= 1;
//   day -= 1;
// }

// let value = document.getElementById("inputslider").getAttribute("value");

// let output = document.getElementById("date");

// let slider = document.getElementById("inputslider");

// slider.oninput = function () {
//   if ((value = 100)) {
//     let date = Date();
//     document.getElementById("text").setAttribute("value", date);
//     output.innerHTML = this.value;
//   }
// };
