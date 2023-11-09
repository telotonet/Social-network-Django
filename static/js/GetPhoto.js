var photoModalhtml =  $('#photoModal')
var photoModal = new bootstrap.Modal(photoModalhtml);

function get_photo_modal(event){
    photoModal.show();
    photoModalhtml.find('img').attr('src', event.target.src)
}