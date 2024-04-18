import json
from model import Response, Ticket, db
from pprint import pprint


def test_get_response(client):

    url = "/api/response/1"
    res = client.get(url)
    json_data = json.loads(res.data)
    pprint(json_data)
    assert res.status_code == 200
    assert len(json_data['response_list']) == 4


def test_get_response_error(client):
    url = "/api/response/9999"
    res = client.get(url)
    json_data = json.loads(res.data)
    # pprint(json_data)
    assert res.status_code == 404
    assert json_data['error_code'] == 'RESPONSE001'


def test_post_response(client):
    url = "/api/response/1"
    payload = {
        "user_id": 1,
        "response": "Test Response"
    }
    res = client.post(url, json=payload)
    json_data = json.loads(res.data)
    assert res.status_code == 201
    assert json_data['ticket_id'] == 1
    obj = Response.query.filter_by(response=payload['response']).first()
    db.session.delete(obj)
    db.session.commit()


def test_post_response_error(client):
    # 404 status code test
    url = "/api/response/9999"
    payload = {
        "user_id": 1,
        "response": "Test Response"
    }
    res = client.post(url, json=payload)
    json_data = json.loads(res.data)
    assert res.status_code == 404
    assert json_data['error_code'] == 'RESPONSE001'
    # 400 status code test
    url = "/api/response/1"
    payload = {
        "response": "Test Response"
    }
    res = client.post(url, json=payload)
    json_data = json.loads(res.data)
    assert res.status_code == 400
    assert json_data['error_code'] == 'RESPONSE003'

    url = "/api/response/1"
    payload = {
        "user_id": 1
    }
    res = client.post(url, json=payload)
    json_data = json.loads(res.data)
    assert res.status_code == 400
    assert json_data['error_code'] == 'RESPONSE003'


def test_put_response(client):
    url = "/api/response/1/4"
    payload = {
        "isAnswer": True,
        "ticket_status": "resolved"
    }
    res = client.put(url, json=json.dumps(payload))
    json_data = json.loads(res.data)
    assert res.status_code == 200


def test_put_response_error_1(client):
    url = "/api/response/9999/4"
    payload = {
        "isAnswer": False,
        "ticket_status": "unresolved"
    }
    res = client.put(url, json=json.dumps(payload))
    json_data = json.loads(res.data)
    assert res.status_code == 404
    assert json_data['error_code'] == 'RESPONSE001'


def test_put_response_error_2(client):
    url = "/api/response/1/999"
    payload = {
        "isAnswer": False,
        "ticket_status": "unresolved"
    }
    res = client.put(url, json=json.dumps(payload))
    json_data = json.loads(res.data)
    assert res.status_code == 404
    assert json_data['error_code'] == 'RESPONSE002'


def test_put_response_error_3(client):
    url = "/api/response/1/4"
    payload = {
        "ticket_status": "resolved"
    }
    res = client.put(url, json=json.dumps(payload))
    json_data = json.loads(res.data)
    assert res.status_code == 400
    assert json_data['error_code'] == 'RESPONSE004'


def test_put_response_error_4(client):
    url = "/api/response/1/4"
    payload = {
        "isAnswer": False,
    }
    res = client.put(url, json=json.dumps(payload))
    json_data = json.loads(res.data)
    assert res.status_code == 400
    assert json_data['error_code'] == 'RESPONSE005'


def test_put_response_error_5(client):
    url = "/api/response/1/4"
    payload = {
        "isAnswer": False,
        "ticket_status": "hello"
    }
    res = client.put(url, json=json.dumps(payload))
    json_data = json.loads(res.data)
    assert res.status_code == 400
    assert json_data['error_code'] == 'RESPONSE006'
