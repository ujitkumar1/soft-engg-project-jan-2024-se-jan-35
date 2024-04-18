# import json


# def test_create_user_student(client):
#     # Set up test data
#     new_user = {'username': 'testuser', 'password': 'testpassword',
#                 'email': 'testuser@gmail.com', 'role': 'student'}
#     email = new_user['email']
#     # Make POST request to create new user
#     response = client.post('/api/register', json=new_user)

#     # Check status code of response
#     assert response.status_code == 201

#     # Check response body for correct username
#     assert json.loads(response.data)['username'] == 'testuser'
#     response = client.delete(f'/api/login/{email}')


# def test_create_user_staff(client):
#     # Set up test data
#     new_staff = {'username': 'teststaff', 'password': 'testpass',
#                  'email': 'teststaff@gmail.com', 'role': 'staff', 'subject_id': 1}
#     email_staff = new_staff['email']
#     # Make POST request to create new user
#     response = client.post('/api/register', json=new_staff)
#     client.delete(f'/api/login/{email_staff}')
#     # Check status code of response
#     assert response.status_code == 201

#     # Check response body for correct username
#     assert json.loads(response.data)['username'] == 'teststaff'
#     assert json.loads(response.data)['email'] == 'teststaff@gmail.com'


# def test_login(client):
#     email = 'user1@gmail.com'
#     response = client.get(f'/api/login/{email}')
#     assert response.status_code == 200


# def test_put_user(client):
#     email = 'user1@gmail.com'
#     response = client.put(
#         f'/api/login/{email}', json={'password': 'user1pass', 'role': 'student'})
#     assert response.status_code == 202
#     assert json.loads(response.data)['password'] == 'user1pass'
