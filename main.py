from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import os, joblib, json, numpy as np

app = FastAPI()

# 掛載靜態文件目錄
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/models", StaticFiles(directory="models"), name="models")

# 設置模板目錄
templates = Jinja2Templates(directory="templates")

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

def PredictGesture(data):
    parameter = scaler.transform([data])
    predict = model.predict(parameter)
    gesture = labels[predict[0]]

   # print(gesture)
    return(gesture)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """首頁，回傳 index.html"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 端點，用於處理即時手勢數據"""
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            data = json.loads(data)
            data = np.array(data)
            gesture = PredictGesture(data)
            #print("收到數據:", data)
            await websocket.send_text(f"手勢: {gesture}")
        except Exception as e:
            print("WebSocket 連線錯誤:", e)
            break
