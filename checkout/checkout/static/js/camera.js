document.addEventListener("DOMContentLoaded", function () {

    const video = document.getElementById('video-display');
    const canvas = document.getElementById('canvas-photo');
    const errorMsgElement = document.querySelector('span#errorMsg');
    const context = canvas.getContext('2d');
    const photo_button = document.getElementById('photo-button');

//obsluga kamery internetowej
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

//metoda obslugujaca event po kliknieciu przycisku Zrob zdjecie
    photo_button.addEventListener("click", function () {
        context.drawImage(video, 0, 0, 300, 150);
        context.imageSmoothingEnabled = true;
        let html = `
        <button id="predict-button">Rozpoznaj</button>`;
        //dynamiczne dodanie przycisku Rozpoznaj
        document.querySelector('#predict-button-div').innerHTML = html;
        const predict_button = document.getElementById('predict-button');
        let image = canvas.toDataURL('image/jpeg');
        let date = new Date().toLocaleString();
        //metoda obslugujaca event po kliknieciu przycisku Rozpoznaj
                predict_button.addEventListener("click", function () {
            $.ajax({
    url         : "/",
    method      : "post",
    contentType : 'application/json',
    dataType    : 'html',
    data        : JSON.stringify({ "imageData": canvas.toDataURL('image/jpeg'), "name" : date })
});
        let html2 = `<a class="link-title" href="/results"><button id="next-button">Dalej</button></a>`;
        //dynamiczne dodanie przycisku Dalej
        document.querySelector('#next-button-div').innerHTML = html2;
        })
    })
})