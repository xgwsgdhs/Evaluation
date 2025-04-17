import os
import app.models
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from app.database import Base, engine

# 加载 .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_ROOT_URI = os.getenv("DB_ROOT_URI")

# 创建不带数据库名的引擎
admin_engine = create_engine(DB_ROOT_URI, echo=True, pool_pre_ping=True)

def create_database_if_not_exists():
    with admin_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"))
        print(f"✅ 数据库 `{DB_NAME}` 已确保存在。")

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ 所有表已自动创建完成。")

if __name__ == "__main__":
    create_database_if_not_exists()
    create_tables()  # 建表调用

