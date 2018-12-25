document.addEventListener("DOMContentLoaded", function(event) {
  let options = document.getElementById('options');
  var elems = document.querySelectorAll('.datepicker');
  var instances = M.Datepicker.init(elems, options);
});
function removeAlert(close){
  close.parentNode.parentNode.removeChild(close.parentNode);
}
function keypress(e){
  e.preventDefault();
}
