document.addEventListener("DOMContentLoaded", function(event) {
        let addButton = document.getElementById('add_button');
        addButton.addEventListener('click', function(){
                let form = '<div class="row">\
                <form class="col s12" action="/add" method = "get">\
                  <div class="row">\
                    <div class="input-field col s12">\
                      <textarea name="title" id="title" class="materialize-textarea"></textarea>\
                      <label for="title">제목</label>\
                    </div>\
                  </div>\
                  <div class="row">\
                    <div class="input-field col s12">\
                      <textarea name="content" id="content" class="materialize-textarea"></textarea>\
                      <label for="content">내용</label>\
                    </div>\
                  </div>\
                  <input type = "submit" class="waves-effect waves-light btn" id="submit_button" value="제출"/>\
                </form>\
              </div>';
                let options = document.getElementById('options');
                options.innerHTML += form;
        });
});