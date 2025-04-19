from pydantic import BaseModel, Field
from typing import Optional


class EvaluationInput(BaseModel):
    name: str = Field(..., description="被评估人姓名")
    score1: int = Field(0, ge=0, le=5)
    score2: int = Field(0, ge=0, le=5)
    score3: int = Field(0, ge=0, le=5)
    score4: int = Field(0, ge=0, le=5)
    score5: int = Field(0, ge=0, le=5)
    score6: int = Field(0, ge=0, le=5)
    score7: int = Field(0, ge=0, le=5)
    score8: int = Field(0, ge=0, le=5)
    score9: int = Field(0, ge=0, le=5)
    score10: int = Field(0, ge=0, le=5)


class EvaluationOutput(EvaluationInput):
    total: int = Field(..., description="总分")
    level: str = Field(..., description="等级：优秀/良好/一般/较差")
    status_code: int = Field(..., description="状态")