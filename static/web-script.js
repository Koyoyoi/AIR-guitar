const socket = io.connect("https://air-guitar.onrender.com", { transports: ["websocket"] });

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        const video = document.createElement("video");
        video.srcObject = stream;
        video.play();

        video.addEventListener("loadedmetadata", () => {
            // 設定 canvas 固定大小
            const canvas = document.createElement("canvas");
            canvas.width = 1080;
            canvas.height = 720;
            const ctx = canvas.getContext("2d");

            setInterval(() => {
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                const imageData = canvas.toDataURL("image/jpeg");
                socket.emit("image", imageData);
            }, 50);
        });
    })
    .catch(error => console.error("無法存取攝影機:", error));

// 接收處理後的影像並顯示
socket.on("processed_image", function(data) {
    document.getElementById("output").src = data;
});
