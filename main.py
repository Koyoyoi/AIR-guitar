from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import cv2, numpy as np, base64
import os, cv2, joblib, time
import handCompute as hc, MPClass as mp

# Path of model, scaler and label
dirName = "numberPos"
modelPath = f"models/{dirName}/svm_{dirName}_model.pkl"
scalerPath = f"models/{dirName}/scaler_{dirName}.pkl"
labelPath = f"models/{dirName}/labels.txt"
    
# Load model, scaler, label
model = joblib.load(modelPath)
scaler = joblib.load(scalerPath)
with open(labelPath, 'r') as f: readData = f.readlines()
labels = [label.strip() for label in readData]

models = [name for name in os.listdir("models") if os.path.isdir(os.path.join("models", name))]
modelIndex = models.index(dirName)

findHands = mp.Hands(2, 0.5, 0.5)
findAction = mp.Pose(0.5, 0.5)

capo = 0

pluck = []
prevPluck = []
prevGesture = None

txtFont = cv2.FONT_HERSHEY_SIMPLEX
txtStroke = cv2.LINE_AA
colorTab = {"Red": (0,0,255), "Green": (0,255,0),}
lastestTime = time.time()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html",  {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    prevGesture = None
    while True:
        try:
            data = await websocket.receive_text()

            img_data = base64.b64decode(data.split(',')[1])
            np_arr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            cv2.resize(frame, (240, 180))
            frame = cv2.flip(frame, 1)
            window = { "h": frame.shape[0], "w": frame.shape[1]}
            handData = findHands.Marks(frame, window["h"], window["w"], depth=1)
            
            # Left hand controll of Gesture predict
            if handData["left"] != []:
                parameter = hc.compute(handData["left"])
                parameter = scaler.transform([parameter])
                predict = model.predict(parameter)
                gesture = labels[predict[0]]   
                if prevGesture != gesture:
                    prevGesture = gesture
                cv2.putText(frame, f"{gesture}", (30, 60), txtFont, 2, colorTab["Red"], 2, txtStroke) 

            _, buffer = cv2.imencode('.jpg', frame)
            flipped_base64 = base64.b64encode(buffer).decode('utf-8')
            
            await websocket.send_text(f"data:image/jpeg;base64,{flipped_base64}")
        except Exception as e:
            print("WebSocket Error:", e)
            break
