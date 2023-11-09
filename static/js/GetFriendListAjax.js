


function getFriendListAjax() {
    if (userCache.hasOwnProperty('friendList')) {
        var friendList = userCache['friendList'];
        getFriendListAjaxHandler(friendList);
    } else {
        $.ajax({
            url: 'http://' + window.location.host + '/friends/',
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                userCache['friendList'] = response;
                getFriendListAjaxHandler(response)
            },
                error: function(xhr, status, error) {
                errorToast('Не удалось запросить список пользователей.')
                console.error(error); // Вывод сообщения об ошибке в консоль
            }
        });
    }
}

function getFriendListAjaxHandler(userData) {
    modalFriends = $('#modalFriends')
    myModalFriends = new bootstrap.Modal(modalFriends);
    modalFriendForCard = $('#modalFriendForCard');
    modalFriendForCard.empty();

    userData.forEach(function(user) {
        var userlink = $('<div>')
            .attr('id', 'userlink')
            .addClass('card-body d-flex mt-1 mb-1 text-decoration-none user-select-none')
            .data('user', JSON.stringify(user)) // Сериализуем объект пользователя в строку JSON
            .click(function() {
                var userData = JSON.parse($(this).data('user')); // Разбираем строку JSON для получения объекта пользователя
                chatAddFriend(userData); // Передаем объект пользователя
            });
        var avatarPlaceholder = $('<div>')
            .addClass('avatar-placeholder rounded-circle user-select-none');
        var profilePhoto = $('<img>')
            .css('object-fit', 'cover')
            .attr('src', user.profile.photo)
            .addClass('profile-photo rounded-circle');
        var textContainer = $('<div>')
            .addClass('text-white w-100');
        var username = $('<p>')
            .addClass('mb-0 mt-1')
            .css('margin-left', '10px')
            .text(user.username);
        userlink.append(avatarPlaceholder);
        avatarPlaceholder.append(profilePhoto);
        userlink.append(textContainer);
        textContainer.append(username);
        modalFriendForCard.append(userlink);
    });
    myModalFriends.show()
}



function chatAddFriend(user){

    $.ajax({
        url: `add_user/${user.id}/`,
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            chatAddFriendHandler(response, user)
        },
            error: function(xhr, status, error) {
            errorToast('Не удалось добавить пользователя.')
            console.error(error); // Вывод сообщения об ошибке в консоль
        }
    });
}

function chatAddFriendHandler(response, userData){
    userDataElement = document.getElementById('userData')
    if (response.status=='delete'){
        $(`[user-id=${userData.id}]`).remove()
    } else if (response.status='add '){
        userDataElement.innerHTML += `<div id="userlink" type="usermodal" user-id="${userData.id}" class="card-body d-flex ">
            <div class="avatar-placeholder rounded-circle">
                <img id="${userData.id}_photo" style="object-fit:cover;" class="profile-photo rounded-circle">
                <div id="${userData.id}_status" class="status-indicator" style="background-color: rgb(83, 83, 83); display: none;"></div>
            </div>
            <div class="text-white w-100">
                <p class="mb-0 mt-1" style="margin-left:10px">${userData.username}</p>
                <p class="mb-0"><small id="${userData.id}_status_small" class="small text-white fw-light" style="font-size: 12px;"></small></p>
            </div>
        </div>`
        if (userData.profile.photo != null){
            $(`#${userData.id}_photo`).attr('src', userData.profile.photo)
        }
    }
    get_user_modal()
}