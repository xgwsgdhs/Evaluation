from app.models import User
from app.database import SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

user = User(
    username="admin",
    hashed_password=pwd_context.hash("123456")
)

db.add(user)
db.commit()
db.close()
print("✅ 用户 admin 创建完成")