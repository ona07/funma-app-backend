from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import pickle

app = FastAPI()

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可（本番では制限する）
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

# ARIMAモデルのパス
ARIMA_MODEL_PATH = "arima_model.pkl"

# **ARIMAモデルをロード**
with open(ARIMA_MODEL_PATH, "rb") as f:
    arima_model = pickle.load(f)

@app.get("/hello")
async def hello():
    return {"message": "hello world!"}

@app.get("/predict")
async def predict():
    """8時間分の15分ごとの合計客数を返す（日本時間対応, 0, 15, 30, 45分固定）"""
    now_utc = datetime.utcnow() + timedelta(hours=9)  # 日本時間（JST）に変換
    now_jst = now_utc.replace(minute=0, second=0, microsecond=0)  # 「00分」にリセット
    predictions = []

    # **未来の混雑率を予測**
    future_steps = 32  # 8時間分（15分ごとに32データ）
    future_predictions = arima_model.forecast(steps=future_steps)  # ARIMAによる予測

    for i in range(future_steps):
        time_jst = now_jst + timedelta(minutes=15 * i)
        formatted_time = time_jst.strftime("%Y-%m-%d %H:%M")
        predicted_count = max(0, future_predictions[i])  # 負の値を防ぐため max(0, x)

        predictions.append({"time": formatted_time, "count": round(predicted_count, 2)})

    return {"predictions": predictions}
