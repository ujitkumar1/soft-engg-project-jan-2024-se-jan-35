# import json
# from pprint import pprint
# from model import Ticket, db


# def test_get_tickets(client):
#     params = {
#         "limit": 3,
#         "TagName": "week 1",
#         "search": "titl"
#     }
#     url = "/api/subject/subject_1"
#     res = client.get(url, query_string=params)
#     json_data = json.loads(res.data)
#     # pprint(json_data)
#     assert res.status_code == 200
#     assert len(json_data) <= params["limit"]
#     for obj in json_data:
#         assert obj['subject_name'] == "subject_1"
#         assert obj["sec_name"] == params['TagName']
#         assert params['search'].lower() in obj['title'].lower()


# def test_get_tickets_error(client):
#     url = "/api/subject/NotASubject"
#     res = client.get(url)
#     assert res.status_code == 404
#     json_data = json.loads(res.data)
#     assert json_data['error_code'] == 'TICKET006'


# def test_create_ticket(client):
#     # Set up test data
#     new_ticket = {
#         "title": "title-ba",
#         "description": "desc-ba",
#         "secondary_tag": "week-1",
#         "user_id": 1
#     }
#     tag_name = "BA"
#     # Make POST request to create new ticket
#     response = client.post(f'/api/subject/{tag_name}', json=new_ticket)

#     # Check status code of response
#     assert response.status_code == 201

#     # Check response body for correct username
#     ticket_obj = json.loads(response.data)
#     ticket_id = ticket_obj['ticket_id']
#     client.delete(f'/api/subject/ticket/{ticket_id}')
#     assert ticket_obj['title'] == 'title-ba'


# def test_mark_resolved_ticket_as_faq(client):
#     # Preconditions-corresponding to ticket_id=1, the ticket_Status should be resolved. user_id =4 should also correspond to staff
#     action_detail = {
#         "action": "faq",
#         "user_id": 4
#     }

#     ticket_id = 1

#     response = client.put(
#         f'/api/subject/ticket/{ticket_id}', json=action_detail)
#     ticket_obj = json.loads(response.data)
#     assert response.status_code == 200
#     assert ticket_obj['isFAQ'] == True
#     obj = Ticket.query.filter_by(ticket_id=ticket_id).first()
#     obj.isFAQ = False
#     db.session.commit()


# def test_mark_unresolved_ticket_as_faq(client):
#     # Preconditions-corresponding to ticket_id=2, the ticket_Status should be unresolved. user_id =4 should also correspond to staff
#     action_detail = {
#         "action": "faq",
#         "user_id": 4
#     }

#     ticket_id = 2
#     response = client.put(
#         f'/api/subject/ticket/{ticket_id}', json=action_detail)
#     error = json.loads(response.data)['error_code']
#     assert response.status_code == 400
#     assert error == "TICKET002"


# def test_ticket_like(client):
#     action_detail = {
#         "action": "like",
#         "user_id": 1
#     }
#     ticket_id = 1

#     response = client.put(
#         f'/api/subject/ticket/{ticket_id}', json=action_detail)
#     ticket_obj = json.loads(response.data)

#     assert response.status_code == 200
#     assert ticket_obj['likes'] == 1
#     response = client.put(
#         f'/api/subject/ticket/{ticket_id}', json=action_detail)
#     ticket_obj = json.loads(response.data)
#     assert response.status_code == 200
#     assert ticket_obj['likes'] == 0
