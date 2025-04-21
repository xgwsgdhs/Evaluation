import pandas as pd
from fastapi import HTTPException
from app.models import Evaluation  # 你的数据库模型
from sqlalchemy.orm import Session
from app.logic import calculate_total_and_level
from app.schemas import EvaluationInput

def handle_excel_file(file, db: Session):
    """
    处理上传的 Excel 文件，解析数据并保存到数据库中。
    :param file: 上传的 Excel 文件
    :param db: 数据库会话
    :return: 处理结果
    """
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="只支持 .xlsx 文件")

    try:
        # 保存上传的文件
        contents = file.file.read()
        with open(f"temp_{file.filename}", "wb") as f:
            f.write(contents)

        # 使用 pandas 解析 Excel 文件
        df = pd.read_excel(f"temp_{file.filename}")

        # 确保文件中至少有11列
        if df.shape[1] < 11:
            raise HTTPException(status_code=400, detail="Excel 文件缺少必要的列")

        # 只读取前 11 列：第一列是姓名，后面 10 列是评分
        df = df.iloc[:, :11]

        # 假设 Excel 文件的第一列是姓名，后面 10 列是评分
        for index, row in df.iterrows():
            name = row.iloc[0]  # 第一列是姓名
            scores = row.iloc[1:11]  # 后面 10 列是评分
            # 将 `/` 替换为 None
            scores = [None if score == '/' else score for score in scores]

            if len(scores) != 10:
                raise HTTPException(status_code=400, detail="评分数据不完整")

            # 查询数据库中是否已存在该姓名
            existing_evaluation = db.query(Evaluation).filter(Evaluation.name == name).first()

            if existing_evaluation:
                # 如果数据已存在，更新现有记录
                existing_evaluation.score1 = scores[0]
                existing_evaluation.score2 = scores[1]
                existing_evaluation.score3 = scores[2]
                existing_evaluation.score4 = scores[3]
                existing_evaluation.score5 = scores[4]
                existing_evaluation.score6 = scores[5]
                existing_evaluation.score7 = scores[6]
                existing_evaluation.score8 = scores[7]
                existing_evaluation.score9 = scores[8]
                existing_evaluation.score10 = scores[9]
            else:
                # 如果数据不存在，插入新的记录
                new_evaluation = Evaluation(
                    name=name,
                    score1=scores[0],
                    score2=scores[1],
                    score3=scores[2],
                    score4=scores[3],
                    score5=scores[4],
                    score6=scores[5],
                    score7=scores[6],
                    score8=scores[7],
                    score9=scores[8],
                    score10=scores[9]
                )
                db.add(new_evaluation)

        db.commit()

        return {"message": "文件上传并处理成功","status_code":200}


    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

def generate_excel(db: Session, file_path: str):
    """
    根据数据库中的评估数据生成 Excel 文件。
    :param db: 数据库会话
    :param file_path: 保存的文件路径
    """
    # 查询所有评分记录
    records = db.query(Evaluation).all()

    # 准备数据：将查询结果转为字典
    data = []
    for r in records:
        input_data = EvaluationInput(**r.__dict__)
        total, level = calculate_total_and_level(input_data)
        data.append({
            "name": r.name,
            "score1": r.score1,
            "score2": r.score2,
            "score3": r.score3,
            "score4": r.score4,
            "score5": r.score5,
            "score6": r.score6,
            "score7": r.score7,
            "score8": r.score8,
            "score9": r.score9,
            "score10": r.score10,
            "total": total,
            "level": level
        })

    # 将数据转换为 DataFrame
    df = pd.DataFrame(data)

    # 生成 Excel 文件并保存
    df.to_excel(file_path, index=False, engine='openpyxl')

    return file_path