from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import web, get_db


QUEST_OBJ = {
        "id": 1,
        "question": "test question",
        "answer": "test answer",
        "value": 100,
        "airdate": "2012-09-25T19:00:00Z",
        "created_at": "2012-09-25T19:00:00Z",
        "updated_at": "2012-09-25T19:00:00Z",
        "category_id": 1,
    }


web.dependency_overrides[get_db] = lambda: Mock()
client = TestClient(web)


def test_questions():
    with patch('app.service.get_questions') as mock_get_questions:
        mock_get_questions.return_value = (QUEST_OBJ, 1)

        response = client.post("/", json={"questions_num": 1})

        assert response.status_code == 200
        assert response.json() == QUEST_OBJ
