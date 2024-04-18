# import json


# def test_role_no_query(client):
#     # Make a GET request to Role API
#     response = client.get('/api/role')
#     # Check status of response
#     assert response.status_code == 200


# def test_role_query_status_true(client):
#     # Make a GET request to Role API
#     response = client.get('/api/role?status=1')
#     # Check status of response
#     assert response.status_code == 200


# def test_role_query_status_false(client):
#     # Make a GET request to Role API
#     response = client.get('/api/role?status=0')
#     # Check status of response
#     assert response.status_code == 200


# def test_edit_role(client):
#     # Dummy Staff data
#     staff_data = {"username": "dummy_satff", "email": "dummy_satff@gmail.com",
#                   "password": "abcd3", "role": "staff", 'subject_id': 1}
#     # Create a new Staff account
#     response = client.post('/api/register', json=staff_data)
#     # Check for response status code
#     assert response.status_code == 201

#     # Extract user-id and make a PUT request
#     staff_data = json.loads(response.data)
#     response = client.put(f"/api/role/{staff_data['user_id']}",
#                           json={'status': True})
#     # Check for response status code
#     assert response.status_code == 202
#     # Check for response data
#     assert json.loads(response.data)['approved'] == True

#     # Remove Dummy data from DB
#     client.delete(f"/api/role/{staff_data['user_id']}")


# def test_delete_role(client):
#     # Dummy Staff data
#     staff_data = {"username": "dummy_satff", "email": "dummy_satff@gmail.com",
#                   "password": "abcd3", "role": "staff", 'subject_id': 1}
#     # Create a new Staff account
#     response = client.post('/api/register', json=staff_data)
#     # Check for response status code
#     assert response.status_code == 201

#     # Extract user-id and make a DELETE request
#     staff_data = json.loads(response.data)
#     response = client.delete(f"/api/role/{staff_data['user_id']}")
#     # Check for response status code
#     assert response.status_code == 200
