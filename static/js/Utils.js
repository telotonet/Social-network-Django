function errorToast(errorText){
    var toastElement = $('#liveToast')
    var toast = new bootstrap.Toast(toastElement)
    var toastBody = $('#toastBody')
    toastBody[0].innerHTML = errorText
    toast.show()
}