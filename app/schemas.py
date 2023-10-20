from datetime import datetime
from pydantic import BaseModel


class QuestionsRequest(BaseModel):
    questions_num: int


class QuestionsResponse(BaseModel):
    id: int
    question: str
    answer: str
    value: int
    airdate: datetime
    created_at: datetime
    updated_at: datetime
    category_id: int
