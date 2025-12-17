def test_delete_todo(session, base_url):
    res = session.delete(f"{base_url}/todos/1")
    assert res.status_code == 200