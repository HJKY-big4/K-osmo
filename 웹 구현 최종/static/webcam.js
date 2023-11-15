// webcam.js
var video = document.querySelector('img');
var toggleButton = document.getElementById('toggle-button');
var captureButton = document.getElementById('capture-button');
var streaming = false;

toggleButton.onclick = function() {
    streaming = !streaming;
    if (streaming) {
        video.src = "{{ video_feed_url }}";
        toggleButton.textContent = "카메라 종료";
    } else {
        video.src = "{{ black_image_url }}";
        toggleButton.textContent = "카메라 시작";
    }
};

captureButton.onclick = function() {
    if (streaming) {
        var fileName = 'photo.jpg';
        var canvas = document.createElement('canvas');
        canvas.width = video.width;
        canvas.height = video.height;
        var ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        var imageData = canvas.toDataURL('image/jpeg');

        $.post("/capture", { image_data: imageData, file_name: fileName }, function(data) {
            console.log(data);
        });
    } else {
        alert("카메라를 먼저 시작해주세요.");
    }
};
