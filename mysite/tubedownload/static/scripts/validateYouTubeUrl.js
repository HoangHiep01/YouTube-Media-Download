function validateYouTubeUrl(event){
    console.log(event.target.value);
    urlToParse = event.target.value
    var btnSubmit = document.getElementById('submit-link');
    if (urlToParse) {
        var regExp = /^(?:https?:\/\/)?(?:m\.|www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
        if (urlToParse.match(regExp)) {
            btnSubmit.classList.remove('disabled');
            return true;
            }
        }
        else {
            btnSubmit.classList.add('disabled');
            return false;
        }
}