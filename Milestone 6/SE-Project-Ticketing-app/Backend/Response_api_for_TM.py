import json

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, fields, marshal_with

from custom_error import LogicError
from model import Response, Secondary_Tag, Subject_Tag, Ticket, User, db


class Responses_api(Resource):
    '''API for getting Ticket responses'''

    response_output = {'ticket_id': fields.Integer, 'title': fields.String,
                       'description': fields.String, 'isFAQ': fields.Boolean,
                       'user_id': fields.Integer, 'ticket_status': fields.String,
                       "subject_name": fields.String(attribute=lambda x: Subject_Tag.query.filter_by(subject_id=x.subject_id).first().subject_name),
                       "sec_name": fields.String(attribute=lambda x: Secondary_Tag.query.filter_by(sec_tag_id=x.sec_id).first().sec_tag_name),
                       'likes': fields.Raw(attribute=lambda x: [i.user_id for i in x.likes]),
                       'response_list': fields.Raw(attribute=lambda x:
                                                   [{
                                                       'response_id': r.response_id,
                                                       'user_id': r.user_id,
                                                       'username': User.query.filter_by(user_id=r.user_id).first().username,
                                                       'response': r.response,
                                                       'isAnswer': r.isAnswer}
                                                    for r in x.response_list
                                                    ])}

    @jwt_required()
    @marshal_with(response_output)
    def get(self, ticket_id: int):

        que = Ticket.query.filter_by(ticket_id=ticket_id).first()

        if que:
            return que, 200
        else:
            raise LogicError(status_code=404, error_code="RESPONSE001",
                             error_msg="Invalid ticket id")

    @jwt_required()
    @marshal_with(response_output)
    def post(self, ticket_id: int):

        obj = Ticket.query.filter_by(ticket_id=ticket_id).first()

        if obj:
            form = request.get_json()
            user_id = form.get("user_id")
            response = form.get("response")
            if user_id is None or response is None:
                raise LogicError(status_code=400, error_code="RESPONSE003",
                                 error_msg="Either user id or response is missing")
            response_obj = Response(user_id=form.get("user_id"),
                                    response=form.get("response"),
                                    ticket_id=ticket_id,
                                    isAnswer=False)
            db.session.add(response_obj)
            db.session.commit()

            que = Ticket.query.filter_by(ticket_id=ticket_id).first()

            return que, 201
        else:
            raise LogicError(status_code=404, error_code="RESPONSE001",
                             error_msg="Invalid ticket id")

    @jwt_required()
    @marshal_with(response_output)
    def put(self, ticket_id: int, response_id: int):

        obj = Response.query.filter_by(
            response_id=response_id, ticket_id=ticket_id).first()

        if obj is None:
            raise LogicError(status_code=404, error_code="RESPONSE002",
                             error_msg="Invalid response id")
        else:
            form = request.get_json()
            print(form)
            if form.get("isAnswer") is None:
                raise LogicError(status_code=400, error_code="RESPONSE004",
                                 error_msg="'isAnswer' field is missing or invalid format")

            que = Ticket.query.filter_by(ticket_id=ticket_id).first()
            if que is None:
                raise LogicError(status_code=404, error_code='RESPONSE001',
                                 error_msg="Invalid ticket id")
            ticket_status = form.get('ticket_status')
            if ticket_status is None:
                raise LogicError(status_code=400, error_code='RESPONSE005',
                                 error_msg="'ticket_status' field is missing or invalid format")
            # checking if ticket status is either "unresolved" or "resolved"
            elif (ticket_status.lower() != "unresolved") == (ticket_status.lower() != "resolved"):
                raise LogicError(status_code=400, error_code='RESPONSE006',
                                 error_msg='Invalid value for ticket_status, it should be either \'resolved\' or \'unresolved\'')

            obj.isAnswer = form.get('isAnswer')
            que.ticket_status = form.get('ticket_status').lower()
            db.session.commit()
            if form.get('isAnswer'):
                objects = Response.query.filter_by(
                    ticket_id=ticket_id, isAnswer=True).all()
                for o in objects:
                    if o.response_id != response_id:
                        o.isAnswer = False
            db.session.commit()
            return que, 200
