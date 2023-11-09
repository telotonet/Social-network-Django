var userModalhtml =  $('#userModal')
var userModal = new bootstrap.Modal(userModalhtml);

function get_user_modal(){
    var userButtons = document.querySelectorAll('[type="usermodal"]');
    userButtons.forEach(function(userButton) {
        userButton.addEventListener('click', function() {
            var userId = userButton.getAttribute('user-id');
            userModal.show();
            if (userCache.hasOwnProperty(userId)) {
                var userData = userCache[userId];
                handleUser(userData);
            } else {
                get_user_ajax(userId);  
            }
        });
    });
}
get_user_modal()

function get_user_ajax(userId) {
    $.ajax({
        url: 'http://' + window.location.host + '/user_ajax/' + userId + '/',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
        // Кэшируем данные пользователя
            userCache[userId] = response;
            setTimeout(() => handleUser(response), 200);
        },
            error: function(xhr, status, error) {
            errorToast('Не удалось запросить пользователя.')
            console.error(error); // Вывод сообщения об ошибке в консоль
        }
    });
}


function handleUser(userData) {
    userModalhtml.find('.modal-body').remove()
    userModalhtml.find('.modal-header').remove()
    var modalContent = userModalhtml.find('.modal-content').css('backgroundColor', 'rgb(35,36,40)')
    var modalHeader = $('<div>').addClass('modal-header position-relative border-bottom border-secondary').css('paddingTop','60px').css('backgroundColor', 'rgb(17, 18, 20)')
    var userPhoto = $('<img>').addClass('position-absolute rounded-circle').css('height', '100px').css('width',
     '100px').css('left', '30px').css('bottom', '-40px').css('backgroundColor', '#ccc').css('zIndex', '1').css('border', '6px solid rgb(35,36,40)').attr('src',
     userData.profile.photo).css('objectFit', 'cover');
    var modalBody = $('<div>').addClass('modal-body rounded').css('backgroundColor', 'rgb(35,36,40)').css('padding', '0')
    var modalBodyInfo = $('<div>').addClass('card rounded').css('backgroundColor', 'rgb(12, 12, 12)').css('margin', '50px 15px 15px').css('padding', '10px')
    var modalBodyInfoUsername = $('<strong>').addClass('card-header fs-3').css('color', 'white').text(userData.username).css('border-bottom', '1px solid white').css('backgroundColor', 'rgb(12, 12, 12)')
    var modalBodyInfoID = $('<p>').css('color', 'white').css('fontSize', '12px').css('fontWeight', '100').text('User ID: ' + userData.id)
    var cardBody = $('<div>').addClass('card-body')
    var cardBodyDateJoinedTitle = $('<Strong>').addClass('card-title').css('color', 'white').text('В числе участников с ')
    var cardBodyDateJoined = $('<p>').text(moment(userData.date_joined).format('MMMM DD, YYYY')).css('color', 'white').css('fontWeight', '100').css('fontSize', '14px')
   
    if (userData.id != requestUserId){
    var friendRequestBtn = $('<button>').addClass('btn position-absolute rounded font-monospace text-wrap').css('font-size', '14px').css('max-width', '200px').css('max-height', '100px').css('zIndex', '1').css('bottom', '-23px').css('right', '50px').css('border', '6px solid rgb(35,36,40)').attr('onclick', "sendFriendRequest(" + userData.id + ")").attr("id", "friend-request_" + userData.id)
    if (userData.is_friend){
        friendRequestBtn.addClass('btn-danger').text('Удалить из друзей')
    } else {
        if (userData.is_friend_request_sent){
            friendRequestBtn.addClass('btn-secondary').text('Отменить запрос')
        } else if  (userData.is_friend_request_received) {
            friendRequestBtn.addClass('btn-warning').text('Принять запрос')
        } else {
            friendRequestBtn.addClass('btn-success').text('Добавить в друзья')
        }
    }}

    if (userData.profile.status){
        var modalBodyInfoStatusTitle = $('<strong>').addClass('card-title').css('color', 'white').text('Обо мне')
        var modalBodyInfoStatus = $('<p>').text(userData.profile.status).css('color', 'white').css('fontWeight', '100').css('fontSize', '14px')
        cardBody.append(modalBodyInfoStatusTitle)
        cardBody.append(modalBodyInfoStatus)
    }
    if (userData.is_superuser){
        modalBodyInfoUsername.prepend('<svg xmlns="http://www.w3.org/2000/svg" style="fill:orange; margin-right:5px;margin-bottom:4px" height="25px" viewBox="0 0 576 512"><path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"/></svg>')
    }
    var goToChatBtnContainer = $('<div>').addClass('d-grid mt-4')
    var goToChatBtn = $('<a>').addClass('btn btn-outline-success').attr('href', `http://${window.location.host}/chat/create/${userData.id}/`).text(`Перейти в чат с ${userData.username}`)
    
    modalHeader.append(userPhoto)
    modalHeader.append(friendRequestBtn)
    modalContent.prepend(modalHeader)
    modalBodyInfoUsername.append(modalBodyInfoID)
    goToChatBtnContainer.append(goToChatBtn)
    cardBody.append(cardBodyDateJoinedTitle)
    cardBody.append(cardBodyDateJoined)
    cardBody.append(goToChatBtnContainer)

    modalBodyInfo.append(modalBodyInfoUsername)
    modalBodyInfo.append(cardBody)

    modalBody.append(modalBodyInfo)
    modalContent.append(modalBody)
}