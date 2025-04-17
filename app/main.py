from fastapi import FastAPI
from app.database import SessionLocal
from sqlalchemy import text
from app import auth
from app import evaluate
app = FastAPI()
app.include_router(auth.router)
app.include_router(evaluate.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/dbtest")
def test_db_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        return {"db": "connected"}
    except Exception as e:
        return {"db": "error", "detail": str(e)}
    finally:
        db.close()