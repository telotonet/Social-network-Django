function sendFriendRequest(user_id) {
    $.ajax({
        url: `/friend-request/${user_id}/`,
        type: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json",
        },
        success: function(data) {
            const toastLive = $('#liveToast')
            const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLive)
            btn = $('#friend-request_' + user_id).removeClass('btn-success').removeClass('btn-secondary').removeClass('btn-danger').removeClass('btn-warning')
            if (data.success==false){
                toastLive.removeAttr('class').addClass('toast text-bg-danger')
            } else {
                switch (data.status){
                    case 'sent': 
                        btn.addClass('btn-secondary')
                        toastLive.removeAttr('class').addClass('toast text-bg-success')
                        message = 'Отменить запрос'
                        break
                    case 'delete':
                        btn.addClass('btn-success')
                        toastLive.removeAttr('class').addClass('toast text-bg-warning')
                        message = 'Добавить в друзья'
                        break
                    case 'accept':
                        btn.addClass('btn-danger')
                        toastLive.removeAttr('class').addClass('toast text-bg-warning')
                        message = 'Удалить из друзей'
                        break
                    case 'decline':
                        btn.addClass('btn-success')
                        toastLive.removeAttr('class').addClass('toast text-bg-warning')
                        message = 'Добавить в друзья'
                        break
                }
                btn.text(message)
            }

            $('#toastBody')[0].innerHTML = data.message
            toastBootstrap.show()
        },
        error: function(xhr, textStatus, errorThrown) {
            // Обработка ошибок
            console.error("Error:", errorThrown);
        }
    });
}
