from app.schemas import EvaluationInput

def calculate_total_and_level(data: EvaluationInput) -> tuple[int, str]:
    """
    评分总分 + 等级判断（每项满分5分，总分满分50）
    """
    scores = [
        data.score1, data.score2, data.score3, data.score4, data.score5,
        data.score6, data.score7, data.score8, data.score9, data.score10
    ]

    total = sum(score if score is not None else 0 for score in scores)

    # 新版等级判断逻辑
    if total >= 40:
        level = "高安全性"
    elif total >= 30:
        level = "中等安全性"
    elif total >= 20:
        level = "低安全性"
    else:
        level = "风险"

    return total, level