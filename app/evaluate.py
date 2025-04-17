from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Evaluation
from app.schemas import EvaluationInput, EvaluationOutput
from app.logic import calculate_total_and_level
from app.auth import get_current_user
from app.models import User
router = APIRouter()

# 依赖项：获取数据库连接
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 创建评分
@router.post("/evaluate", response_model=EvaluationOutput)
def create_evaluation(data: EvaluationInput, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if db.query(Evaluation).filter(Evaluation.name == data.name).first():
        raise HTTPException(status_code=400, detail="用户已存在")

    record = Evaluation(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)

    total, level = calculate_total_and_level(data)
    return {**data.dict(), "total": total, "level": level}

# 🔹 查询所有评分记录
@router.get("/evaluations", response_model=list[EvaluationOutput])
def get_all_evaluations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    records = db.query(Evaluation).all()
    results = []

    for r in records:
        input_data = EvaluationInput(**r.__dict__)
        total, level = calculate_total_and_level(input_data)
        results.append({**input_data.dict(), "total": total, "level": level})

    return results

# 🔹 查询指定用户评分
@router.get("/evaluation", response_model=EvaluationOutput)
def get_evaluation_by_name(name: str = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    r = db.query(Evaluation).filter(Evaluation.name == name).first()
    if not r:
        raise HTTPException(status_code=404, detail="用户不存在")

    input_data = EvaluationInput(**r.__dict__)
    total, level = calculate_total_and_level(input_data)
    return {**input_data.dict(), "total": total, "level": level}

# 🔹 修改评分（通过 name）

@router.put("/evaluation", response_model=EvaluationOutput)
def update_evaluation(name: str = Query(...),data: EvaluationInput = ...,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    r = db.query(Evaluation).filter(Evaluation.name == name).first()
    if not r:
        raise HTTPException(status_code=404, detail="用户不存在")

    for field, value in data.dict().items():
        setattr(r, field, value)

    db.commit()
    db.refresh(r)

    total, level = calculate_total_and_level(data)
    return {**data.dict(), "total": total, "level": level}

# 🔹 删除评分记录
@router.delete("/evaluation")
def delete_evaluation(name: str = Query(...), db: Session = Depends(get_db)):
    r = db.query(Evaluation).filter(Evaluation.name == name).first()
    if not r:
        raise HTTPException(status_code=404, detail="用户不存在")

    db.delete(r)
    db.commit()
    return {"message": f"{name} 的评分记录已删除"}