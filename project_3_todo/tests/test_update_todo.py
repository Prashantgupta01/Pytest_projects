def test_update_todo(session, base_url):
    payload = {
        "userId": 1,
        "title": "Updated ToDo Title",
        "completed": True
    }

    res = session.put(f"{base_url}/todos/1", json=payload)
    assert res.status_code == 200

    data = res.json()
    assert data["completed"] is True
