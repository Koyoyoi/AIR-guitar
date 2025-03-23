import cv2
import base64
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet", transports=["websocket"])

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on("image")
def handle_image(data):
    """ 處理從前端傳來的影像 """
    try:
        encoded_data = data.split(',')[1]  # 移除 `data:image/png;base64,` 的部分
        image_data = base64.b64decode(encoded_data)

        # 轉換為 OpenCV 格式
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 影像處理（轉成灰階）
        _, buffer = cv2.imencode(".jpg", gray)  # 轉換為 JPG 格式
        processed_base64 = base64.b64encode(buffer).decode("utf-8")

        # 傳回處理後的影像
        socketio.emit("processed_image", f"data:image/jpeg;base64,{processed_base64}")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000. debug=True)
