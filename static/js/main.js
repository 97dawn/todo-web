document.addEventListener("DOMContentLoaded", function(event) {
  let options = document.getElementById('options');
  var elems = document.querySelectorAll('.datepicker');
  var instances = M.Datepicker.init(elems, options);
  document.getElementById('add_button').addEventListener('click', function(){
    document.getElementById('submit_button').addEventListener('click', function(){
      if (!document.getElementById('title').value | !document.getElementById('content').value){
        alert('모든 값을 입력해주세요');
      }
    });
  });
});
function removeAlert(close){
  close.parentNode.parentNode.removeChild(close.parentNode);
}
function keypress(e){
  e.preventDefault();
}