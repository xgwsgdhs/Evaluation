from fastapi import APIRouter, HTTPException, Depends, Query, File, UploadFile
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Evaluation
from app.schemas import EvaluationInput, EvaluationOutput
from app.logic import calculate_total_and_level
from app.auth import get_current_user
from app.excel_handler import handle_excel_file
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
    return {**data.dict(), "total": total, "level": level, "status_code": 200}

# 🔹 查询所有评分记录
@router.get("/evaluations", response_model=dict)
def get_all_evaluations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 查询所有评分记录
    records = db.query(Evaluation).all()
    results = []

    # 遍历每个评分记录
    for r in records:
        # 创建 EvaluationInput 对象
        input_data = EvaluationInput(**r.__dict__)

        # 计算总分和等级
        total, level = calculate_total_and_level(input_data)

        # 创建新的字典，将 `total` 和 `level` 添加到响应中
        result = {**input_data.dict(), "total": total, "level": level}

        # 将结果添加到结果列表中
        results.append(result)

    # 返回外层字典，包含 status_code 和 data（评分记录列表）
    return {"status_code": 200, "data": results}

# 🔹 查询指定用户评分
@router.get("/evaluation", response_model=EvaluationOutput)
def get_evaluation_by_name(name: str = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    r = db.query(Evaluation).filter(Evaluation.name == name).first()
    if not r:
        raise HTTPException(status_code=404, detail="用户不存在")

    input_data = EvaluationInput(**r.__dict__)
    total, level = calculate_total_and_level(input_data)
    return {**input_data.dict(), "total": total, "level": level, "status_code": 200}

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
    return {**data.dict(), "total": total, "level": level, "status_code": 200}

# 🔹 删除评分记录
@router.delete("/evaluation")
def delete_evaluation(name: str = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    r = db.query(Evaluation).filter(Evaluation.name == name).first()
    if not r:
        raise HTTPException(status_code=404, detail="用户不存在")

    db.delete(r)
    db.commit()
    return {"message": f"{name} 的评分记录已删除", "status_code": 200}

@router.post("/upload_excel")
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    接收上传的 Excel 文件并解析数据
    """
    result = handle_excel_file(file, db)
    return result