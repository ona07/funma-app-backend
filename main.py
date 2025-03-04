from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
