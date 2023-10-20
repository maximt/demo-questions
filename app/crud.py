from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import models
from app import schemas


def create_question(
    db: Session,
    question: schemas.QuestionsResponse
) -> bool:
    try:
        db_obj = models.Question(**question.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return True
    except IntegrityError as e:
        print(e)
        return False
