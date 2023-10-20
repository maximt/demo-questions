import pytest
from unittest.mock import Mock, patch
from tests.data import QUEST_OBJECTS
from app.schemas import QuestionsResponse
from app import service
from app import crud
from app.service import get_questions, get_questions_from_api


@pytest.fixture
def mock_env():
    with patch("app.service.URL_QUESTIONS_API", "https://test.com"), \
         patch("app.service.RETRIES", 3):
        yield


def test_get_questions_from_api_valid_url(mock_env):
    mock_response = Mock()
    mock_response.json.return_value = QUEST_OBJECTS

    with patch("app.service.httpx.get", return_value=mock_response):
        question = get_questions_from_api(1)

    assert question == QUEST_OBJECTS


def test_get_questions_from_api_url_not_set(mock_env):
    with patch("app.service.URL_QUESTIONS_API", None):
        with pytest.raises(ValueError):
            get_questions_from_api(1)


def test_get_questions_from_api_empty_response(mock_env):
    mock_response = Mock()
    mock_response.json.return_value = []

    with patch("app.service.httpx.get", return_value=mock_response):
        question = get_questions_from_api(1)

    assert question is None


def test_get_questions_success():
    num_questions = len(QUEST_OBJECTS)

    with patch.object(service, "get_questions_from_api", return_value=QUEST_OBJECTS) as mock_get_questions_from_api, \
         patch.object(crud, "create_question", return_value=True) as mock_create_question:
        question, count = get_questions(num_questions, Mock())

    assert question == QuestionsResponse(**QUEST_OBJECTS[-1])
    assert count == num_questions
    assert mock_get_questions_from_api.call_count == 1
    assert mock_create_question.call_count == num_questions


def test_get_questions_no_question():
    num_questions = 3

    with patch.object(service, "get_questions_from_api", return_value=None) as mock_get_questions_from_api, \
         patch.object(crud, "create_question") as mock_create_question:
        question, count = get_questions(num_questions, Mock())

    assert question is None
    assert count == 0
    assert mock_get_questions_from_api.call_count == 1
    assert mock_create_question.call_count == 0


def test_get_questions_api_exception():
    num_questions = 3
    api_exception = Exception("API error")

    with patch.object(service, "get_questions_from_api", side_effect=api_exception) as mock_get_questions_from_api, \
         patch.object(crud, "create_question") as mock_create_question:
        question, count = get_questions(num_questions, Mock())

    assert question is None
    assert count == 0
    assert mock_get_questions_from_api.call_count == 1
    assert mock_create_question.call_count == 0


def test_get_questions_db_exception():
    num_questions = 3
    api_exception = Exception("DB error")

    with patch.object(service, "get_questions_from_api", return_value=QUEST_OBJECTS) as mock_get_questions_from_api, \
         patch.object(crud, "create_question", side_effect=api_exception) as mock_create_question:
        question, count = get_questions(num_questions, Mock())

    assert question is None
    assert count == 0
    assert mock_get_questions_from_api.call_count == 1
    assert mock_create_question.call_count == 1


def test_get_questions_duplicates():
    responses = [
        [QUEST_OBJECTS[0], QUEST_OBJECTS[0], QUEST_OBJECTS[1]],  # dups
        [QUEST_OBJECTS[2]]
    ]

    response_part = iter(responses)
    questions_db = []

    def _get_questions_from_api(num: int):
        return next(response_part)[0:num]

    def _create_question(db, question: QuestionsResponse):
        if question.id in questions_db:
            return False
        questions_db.append(question.id)
        return True

    num_questions = 3

    with patch.object(service, "get_questions_from_api", new=_get_questions_from_api), \
         patch.object(crud, "create_question", new=_create_question):
        question, saved_count = get_questions(num_questions, Mock())

    last_question = responses[-1][-1]
    assert question == QuestionsResponse(**last_question)
    assert saved_count == num_questions


def test_get_questions_duplicates_limit_exceeded(mock_env):
    responses = [
        [QUEST_OBJECTS[0], QUEST_OBJECTS[0], QUEST_OBJECTS[1]],
        [QUEST_OBJECTS[0]],  # dups
        [QUEST_OBJECTS[0]],  # dups
        [QUEST_OBJECTS[0]],  # dups
    ]

    response_part = iter(responses)
    questions_db = []

    def _get_questions_from_api(num: int):
        return next(response_part)[0:num]

    def _create_question(db, question: QuestionsResponse):
        if question.id in questions_db:
            return False
        questions_db.append(question.id)
        return True

    num_questions = 3

    with patch.object(service, "get_questions_from_api", new=_get_questions_from_api), \
         patch.object(crud, "create_question", new=_create_question):
        question, saved_count = get_questions(num_questions, Mock())

    last_unique_question = QUEST_OBJECTS[1]
    assert question == QuestionsResponse(**last_unique_question)
    assert saved_count == 2  # request for 3 questions but have only 2 unique
