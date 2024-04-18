import datetime
import os
import requests as rq
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_restful import Api
from werkzeug.security import check_password_hash

from custom_error import DataError, LogicError
from Login_manager_api import Login_api
from mail_config import send_email
from model import Staff, Subject_Tag, User, db
from Response_api_for_TM import Responses_api
from Role_manager_api import Role_api
from Tag_manager_api import Tag_api
from Ticket_manager_api import Ticket_api
import requests

# Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.getcwd() + \
    '/DB_project.sqlite3'
api = Api(app)

app.config['SECRET_KEY'] = 'FMM-2'
CORS(app)
JWTManager(app)
db.init_app(app)
app.app_context().push()
db.create_all()

# API URLS
api.add_resource(Login_api, '/api/register', '/api/login/<string:email>')
api.add_resource(Role_api, '/api/role', '/api/role/<int:user_id>')
api.add_resource(Ticket_api, '/api/subject/ticket/<int:ticket_id>',
                 '/api/subject/<string:subject_name>')
api.add_resource(Responses_api, '/api/response', '/api/response/<int:ticket_id>',
                 '/api/response/<int:ticket_id>/<int:response_id>')
api.add_resource(Tag_api,
                 '/api/tag/<string:tag_type>', '/api/tag/<string:tag_type>/<int:tag_id>')
webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAAaBileJo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=FFrC6t9XgrHAZMfZvkWnt5YQ_Tr__01JGly9n5kOFPk'

# Controllers

@app.route('/flag_post',methods = ['POST'])
def flag_post():
    #     user-id, ticke_id
    form = request.get_json()
    print(form)
    # current_user = get_jwt_identity()
    # user = User.query.filter_by(username=current_user).first()
    ticket_id = form['ticket_id']
    title = form['ticket_name']

    message = f'''The Ticket has been flaged, please check this. Ticket_id: {ticket_id} Title : {title} Immediate action required!'''

    payload = {
        'text': message
    }
    res = requests.post(webhook_url, json=payload)

    if res:
        return {'status':True}, 200
    else:
        return {'status':False}, 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = request.get_json()
    username = form.get("username")
    password = form.get("password")
    user = User.query.filter_by(username=username).first()
    user_id = int(user.user_id)
    print(user_id, check_password_hash(pwhash=user.password, password=password))
    if not user:
        raise DataError(status_code=404)
    if check_password_hash(pwhash=user.password, password=password):
        if user.role == 'staff':
            staff = Staff.query.filter_by(user_id=user_id).first()
            if staff.status == False:
                raise LogicError(status_code=400, error_code="USER006",
                                 error_msg="The staff is unapproved. Please wait for approval")
            else:
                expire_time = datetime.timedelta(days=1)
                access_token = create_access_token(
                    identity=username, expires_delta=expire_time)
                return {'access_token': access_token, 'role': user.role, "user_id": user.user_id, "subject_name": Subject_Tag.query.filter_by(subject_id=staff.subject_id).first().subject_name}, 200

        expire_time = datetime.timedelta(days=1)
        access_token = create_access_token(
            identity=username, expires_delta=expire_time)
        return {'access_token': access_token, 'role': user.role, "user_id": user.user_id}, 200
    else:
        raise LogicError(status_code=400, error_code="USER005",
                         error_msg="Either username or password is incorrect")


@app.route('/notify/<string:role>', methods=['POST'])
@jwt_required()
def notifyMail(role):
    form = request.get_json()
    ticket_id = form.get('ticket_id')
    if ticket_id is None:
        # if ticket-id is missing raise error
        raise DataError(status_code=400)

    if role == 'student':
        # Sending specific notification to students abt their ticket status
        token = request.headers['Authorization']
        ticket_data = rq.get(request.url_root + 'api/response/' +
                             ticket_id, headers={'Authorization': token}).json()
        author = User.query.filter_by(
            user_id=ticket_data.get('user_id')).first()
        if get_jwt_identity() != author.username:
            # Checking if the ticket's author posted the response then no notfication
            send_email(to=author.email, subject="New response is posted in your ticket",
                       msg=render_template('mail_body_student.html', username=author.username,
                                           response=ticket_data.get('response_list')[-1]))
    else:
        # Sending notification to respective staff that new ticket has been created
        subject_name = form.get('subject_name')
        token = request.headers['Authorization']
        staff_list = rq.get(request.url_root + 'api/role?status=1',
                            headers={'Authorization': token}).json()

        staff_list = filter(lambda x: x.get('subject_name') == subject_name,
                            staff_list)
        ticket_data = rq.get(request.url_root + 'api/response/' +
                             str(ticket_id), headers={'Authorization': token}).json()
        for staff in staff_list:
            # print(staff)
            send_email(to=staff.get('email'), subject="New Ticket is created",
                       msg=render_template('mail_body_staff.html', username=staff.get('username'), ticket=ticket_data))

    return 'Success', 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5500')
