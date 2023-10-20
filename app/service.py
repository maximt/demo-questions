import os
from typing import Any

import httpx
from dotenv import load_dotenv
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.schemas import QuestionsResponse
from app import crud


load_dotenv()


URL_QUESTIONS_API = os.environ.get('URL_QUESTIONS_API')
RETRIES = int(os.environ.get('RETRIES', 3))


def get_questions_from_api(num: int) -> Any:
    if not URL_QUESTIONS_API:
        raise ValueError('URL_QUESTIONS_API is not set')

    response = httpx.get(URL_QUESTIONS_API + str(num))
    result = response.json()
    if result:
        return result
    return None


def get_questions(
    num: int,
    db: Session
) -> (QuestionsResponse | None, int):
    last_question: QuestionsResponse | None = None

    try_count = 0
    saved_count = 0

    try:
        while saved_count < num:
            if try_count > RETRIES:
                print("Limit exceeded")
                break
            try_count += 1

            request_num = num - saved_count
            print("Request for {} questions".format(request_num))

            questions = get_questions_from_api(request_num)

            if not questions:
                print("Cannot to get questions")
                break

            for question in questions:
                try:
                    tmp_question = QuestionsResponse(**question)
                    if (crud.create_question(db, tmp_question)):
                        last_question = tmp_question
                        saved_count += 1
                        print("Question saved: {}".format(tmp_question.id))
                    else:
                        print("Dup for question: {}".format(tmp_question.id))
                except ValidationError as e:
                    print(e)

    except Exception as e:
        print(e)

    print("Question saved count: {}".format(saved_count))
    return last_question, saved_count
