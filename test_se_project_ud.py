
import requests
def test_getUserDetails():

url = 'http://127.0.0.1:5000//api/getUserDetails'
myobj = {'user_id': 1004}
response = requests.post(url, data = myobj)
output = response.json()
expected= {"name": Student_Name,"email":"student@iitm.ds.study.com","role":"support staff","member_since":"Fri, 10 Mar 2022 06:36:58 GMT"}
assert output.name==expected.name


def test_getUserDetails():
    url = 'http://127.0.0.1:5000//api/getUserDetails'
    myobj = {'user_id': 1004}
    response = requests.post(url, data = myobj)
    output = response.json()
    expected= {"name": Student_Name,"email":"student@iitm.ds.study.com","role":"support staff","member_since":"Fri, 10 Mar 2022 06:36:58 GMT"}
    assert type(output.name) != <class 'int'>

def test_getUserDetails():
    url = 'http://127.0.0.1:5000//api//api/getSpamUser'
    myobj = {'user_id': 1004}
    response = requests.post(url, data = myobj)
    output = response.json()
    expected= {"isspam": True,"num_posts":15,"list_posts":[]}
    assert output.isspam==True & output.num_posts>14

def test_getUserDetails():
    url = 'http://127.0.0.1:5000//api//api/getSpamUser'
    myobj = {'user_id': 1005}
    response = requests.post(url, data = myobj)
    output = response.json()
    expected= {"isspam": False,"num_posts":10,"list_posts":[]}
    assert output.isspam==False
    

