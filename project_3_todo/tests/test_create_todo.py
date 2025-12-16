def test_create_todo(session, base_url):
    payload = {
        "userId": 1,
        "title": "Learn PyTest API Testing",
        "completed": False
    }

    res = session.post(f"{base_url}/todos", json=payload)
    assert res.status_code == 201

    data = res.json()
    assert data["userId"] == 1
    # assert data["title"] == "Learn Pytest API Testing"
    assert data["completed"] is False
