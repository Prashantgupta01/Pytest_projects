from jsonschema import validate

def test_get_all_todos(base_url, session):
    res = session.get(f"{base_url}/todos")
    assert res.status_code == 200
    assert len(res.json()) > 0

def test_get_single_todo_schema(session, base_url):
    res = session.get(f"{base_url}/todos/1")
    assert res.status_code == 200

    todo = res.json()

    schema = {
        "type": "object",
        "properties": {
            "userId": {"type": "number"},
            "id": {"type": "number"},
            "title": {"type": "string"},
            "completed": {"type": "boolean"}
        },
        "required": ["userId", "id", "title", "completed"]
    }

    validate(instance=todo, schema=schema)