const canvas = document.createElement("canvas"); // 動態建立 canvas
const ctx = canvas.getContext("2d");
const flippedImage = document.getElementById("flippedImage");
const ws = new WebSocket("wss://air-guitar.onrender.com/ws");

// 啟動攝影機
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        const video = document.createElement("video"); // 不顯示 video
        video.srcObject = stream;
        video.play();

        video.addEventListener("play", () => {
            setInterval(() => {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                const dataURL = canvas.toDataURL("image/jpeg");
                ws.send(dataURL);
            }, 100);
        });
    })
    .catch(err => console.error("攝影機錯誤:", err));

// 接收並顯示翻轉影像
ws.onmessage = event => {
    flippedImage.src = event.data;
};
