from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import pickle
import pandas as pd

app = FastAPI()

# CORSミドルウェア設定（開発用：すべて許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prophetモデルのパス
PROPHET_MODEL_PATH = "prophet_model.pkl"

# Prophetモデルの読み込み
with open(PROPHET_MODEL_PATH, "rb") as f:
    prophet_model = pickle.load(f)

@app.get("/hello")
async def hello():
    return {"message": "hello world!"}

@app.get("/predict")
async def predict():
    """
    現在時刻（JST）から8時間分の混雑予測を返す（15分おき、32ステップ）
    """
    # 現在時刻（JST）を0分に丸める
    now_utc = datetime.utcnow() + timedelta(hours=9)
    start_jst = now_utc.replace(minute=0, second=0, microsecond=0)

    # 15分おきの未来の時刻を32ステップ分生成
    future = pd.date_range(start=start_jst, periods=16, freq="15min")
    future_df = pd.DataFrame({"ds": future})

    # 予測を実行
    forecast = prophet_model.predict(future_df)

    # 結果を整形
    predictions = []
    for _, row in forecast.iterrows():
        predictions.append({
            "time": row["ds"].strftime("%Y-%m-%d %H:%M"),
            "count": round(max(0, row["yhat"]), 2)
        })

    return {"predictions": predictions}

@app.get("/predict2")
async def predict2(start_time: str = Query(None, description="形式: YYYY-MM-DD HH:MM")):
    """
    指定時刻（JST）または現在時刻から8時間分の混雑予測を返す（15分おき、32ステップ）
    """
    try:
        if start_time:
            # 指定された時刻文字列をJSTとして解釈
            start_jst = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        else:
            # 現在のJST時刻を0分に丸めて使用
            now_utc = datetime.utcnow() + timedelta(hours=9)
            start_jst = now_utc.replace(minute=0, second=0, microsecond=0)
    except ValueError:
        return {"error": "Invalid datetime format. Use YYYY-MM-DD HH:MM"}

    # 未来の時刻を生成
    future = pd.date_range(start=start_jst, periods=16, freq="15min")
    future_df = pd.DataFrame({"ds": future})

    # 予測を実行
    forecast = prophet_model.predict(future_df)

    # 結果を整形
    predictions = []
    for _, row in forecast.iterrows():
        predictions.append({
            "time": row["ds"].strftime("%Y-%m-%d %H:%M"),
            "count": round(max(0, row["yhat"]), 2)
        })

    return {"predictions": predictions}
