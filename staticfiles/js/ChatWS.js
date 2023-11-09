// import { MockWebSocket } from 'mock-socket';

setTimeout(() => {
    chatSocket.close();
  }, 5000);
  
var chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/{{chat_id}}/');
    // var chatSocket = new WebSocket('ws://' + window.location.host + '/asd/');
    chatSocket.onmessage = function(event) {
        var data = JSON.parse(event.data);
        var typing = data['typing']
        var message = data['new_message']
        var user_joined = data['user_joined']
        var message_read = data['message_read']
        if (user_joined){
            $(".status-indicator").css("background-color", "rgb(83, 83, 83)").css('display','none');
            $(".small").text('').css('display','none');
            user_joined['connected_users'].forEach(function(el) {
                $("#" + el + "_status").css('backgroundColor', 'rgb(35, 165, 90)').css('display','block');
            });
        }
        if (message) {
            user = JSON.parse(message['user']);
            var sender_id = user.id;
            var messageElement = document.createElement('div');
            if ('{{request.user.id}}' == sender_id){
                messageElement.classList.add('card', 'mb-2', 'bg-danger-subtle', 'w-60', 'float-end');
                messageElement.style.marginLeft = '30%';
                messageElement.style.minWidth = '30%';
                messageElement.style.maxWidth = '80%';
                new_el = `
                    <div class="card-body justify-content-center" style="padding:8px 8px 8px 12px;">
                        <p class="card-text" style="margin:0;">${ message.message }</p>
                        <p class="card-text text-end text-muted fw-light" style="margin:0; padding:0px; line-height: 10px;"><small style='line-height: 10px;' id='${message.message_id}_is_read'></small><small class="text-muted">${ message.timestamp }</small></p>
                    </div>`
                messageElement.innerHTML = new_el;
                document.querySelector('#chat-messages').appendChild(messageElement);
                var chatMessagesContainer = document.querySelector('#chat-messages');
                chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
            } else {
                messageElement.classList.add('card', 'mb-2', 'bg-info-subtle', 'w-60', 'float-start');
                messageElement.style.marginRight = '30%';
                messageElement.style.minWidth = '30%';
                messageElement.style.maxWidth = '80%';
                new_el = `
                    <div class="card-body d-flex" style="padding:8px 8px 8px 12px;">
                        <div class="d-flex align-items-center">
                            <img src="${$('#' + sender_id + '_photo').attr('src')}" class="profile-photo rounded-circle" style="width: 40px; height: 40px;margin-right:12px">
                        </div>
                        <div class="">
                            <p class="card-text" style="margin:0;">${message.message}</p>
                            <p class="card-text text-end text-muted fw-light" style="margin:0; padding:0px; line-height: 10px;">
                                <small style="line-height: 10px;" id="${message.message_id}_is_read"></small>
                                <small class="text-muted">${message.timestamp}</small>
                            </p>
                        </div>
                    </div>`;
                messageElement.innerHTML = new_el;
                document.querySelector('#chat-messages').appendChild(messageElement);
            };
        }
        if (message_read){
            message_id = message_read['message_id']
            $('#'+message_id+'_is_read').text('прочитано ');
        }
        if (typing){
            typing_username = typing['username']
            typing_user_id = typing['typing_user_id']
            is_typing = typing['is_typing']
            if (is_typing){
                $('#' + typing_user_id + '_status').css('width', '30px').css('borderRadius', '10px')
                typingElement = '<div class="spinner-grow bg-black position-relative" style="height:5px; width:5px; top:-9px; right:-4px;margin-right:1px" role="status"></div>'
                for (var i = 0; i < 3; i++) {
                    setTimeout(function() {
                        $('#' + typing_user_id + '_status').append(typingElement);
                    }, i * 200); // Умножаем индекс на 100, чтобы получить задержку в 0.1 секунды
                }
            } else {
                $('#' + typing_user_id + '_status').css('width', '18px').empty()
            }

        }
};

    socket.onclose = function(event) {
        if (event.wasClean) {
            // Соединение было закрыто
            console.log('Соединение закрыто');
        } else {
            // Соединение было некорректно закрыто или произошла ошибка
            console.log('Соединение потеряно');
        }
    };

    afterAll(() => {
        socket.clean();
      });


      