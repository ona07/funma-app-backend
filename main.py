from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import random

app = FastAPI()

# CORS の設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可（制限する場合は ["http://192.168.1.9:3000"]）
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST などをすべて許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

@app.get("/hello")
def hello():
    return {"message": "hello world!"}

@app.get("/predict")
async def predict():
    """8時間分の15分ごとの合計客数を返す（日本時間対応, 0, 15, 30, 45分固定）"""
    now_utc = datetime.utcnow() + timedelta(hours=9)  # 日本時間（JST）に変換
    now_jst = now_utc.replace(minute=0, second=0, microsecond=0)  # 「00分」にリセット
    predictions = []

    for i in range(32):  # 8時間分（15分ごとに32データ）
        time_jst = (now_jst + timedelta(minutes=15 * i))
        formatted_time = time_jst.strftime("%Y-%m-%d %H:%M")  # "YYYY-MM-DD HH:MM" 形式
        count = random.randint(5, 30)  # 5~30人のランダムな客数
        predictions.append({"time": formatted_time, "count": count})

    return {"predictions": predictions}