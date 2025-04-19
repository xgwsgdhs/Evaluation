from fastapi import FastAPI
from app import auth
from app import evaluate
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

# 从环境变量中获取 CORS 允许的源，支持多个地址以逗号分隔
origins = os.getenv("ORIGINS", "").split(",")  # 默认值为空列表，如果没有设置


# 如果没有配置 ORIGINS，提示未设置
if not origins or origins == ['']:
    print("No origins")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的前端 URL
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法（GET, POST 等）
    allow_headers=["*"],  # 允许所有请求头
)

app.include_router(auth.router)
app.include_router(evaluate.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}