import sys

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.schemas import QuestionsRequest, QuestionsResponse
from app.db_session import DBSession
from app import service


if 'initdb' in sys.argv:
    print('initializing db')
    DBSession.create_all()
    exit()


web = FastAPI()


async def get_db():
    sessionLocal = DBSession.sessionLocal()
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@web.post("/")
async def questions(
    request: QuestionsRequest,
    db: Session = Depends(get_db)
) -> QuestionsResponse | None:

    question, _ = service.get_questions(num=request.questions_num, db=db)
    return question
