$('form').submit(function(event) {
    event.preventDefault();  // Отмена стандартной отправки формы

    var form = $(this);
    var formData = new FormData(form[0]);

    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
        if (response.success==true) {
            new_post = `
            <div class="card text-light user-select-none mb-4" style="border-radius: 20px; border: 1px solid rgb(133, 133, 133); background-color: rgb(34, 34, 34);">
            <div class="d-flex usermodal mb-2" style="cursor: pointer; padding: 25px 0px 0px 40px;" type="usermodal" user-id="${response.obj.author.id}">
                <div class="rounded-circle" style="background-image: url(${response.obj.author.profile.photo}); width:50px; height:50px; background-color: #ccc; background-size: cover;" alt=""></div>
                <div class="d-block" style="margin-left: 20px; line-height: 5px; margin-top: 8px; font-size: 15px;">
                    <p>${response.obj.author.username}</з>
                    <p class="text-secondary font-monospace">Только что</p>
                </div>
            </div>
            <div class="card-body text-center" style="padding: 0px 20px 15px 15px">
                Запись успешно добавлена.
            </div>
          </div>
          </div>`
            $('#feed').prepend(new_post)
        } else {
            errorToast(response.message)
        }
        },
        error: function(xhr, errmsg, err) {
        console.log(xhr.status + ': ' + xhr.responseText);  // Вывод ошибки в консоль
        }
    });
});
