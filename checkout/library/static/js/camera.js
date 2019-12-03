document.addEventListener("DOMContentLoaded", function () {

    const video = document.getElementById('video-display');
    const canvas = document.getElementById('canvas-photo');
    const errorMsgElement = document.querySelector('span#errorMsg');
    const context = canvas.getContext('2d');
    const photo_button = document.getElementById('photo-button');



    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia ||
        navigator.msGetUserMedia || navigator.oGetUserMedia;

    if (navigator.getUserMedia) {
        navigator.getUserMedia({
            video: true,
            audio:false
        }, handleVideo, videoError);
    }

    function handleVideo(stream) {
        window.stream = stream;
        video.srcObject = stream;
        video.play();

    }

    function videoError(e) {
        alert("Something went wrong");
    }

    photo_button.addEventListener("click", function () {
        context.drawImage(video, 0, 0, 300, 150);
        context.imageSmoothingEnabled = true;
        let html = `
<button id="predict-button" type="submit" value="Rozpoznaj">Rozpoznaj</button>`;
        document.querySelector('#predict-button-div').innerHTML = html;
        const predict_button = document.getElementById('predict-button');
        //let image = context.getImageData(0, 0, 300, 150);
        let image = canvas.toDataURL('image/jpeg');
        let date = new Date().toLocaleString();
                predict_button.addEventListener("click", function () {
            $.ajax({
    url         : "/",
    method      : "post",
    contentType : 'application/json',
    dataType    : 'html',
    data        : JSON.stringify({ "imageData": canvas.toDataURL('image/jpeg'), "name" : date })
});
        })
    })
})