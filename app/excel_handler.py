import pandas as pd
from fastapi import HTTPException
from app.models import Evaluation  # 你的数据库模型
from sqlalchemy.orm import Session

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