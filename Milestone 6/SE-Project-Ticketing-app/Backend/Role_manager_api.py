from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, fields, marshal_with

from custom_error import DataError, LogicError
from model import Staff, Subject_Tag, db


class Role_api(Resource):
    '''API code for Staff Table'''

    output = {"user_id": fields.Integer, "username": fields.String,
              "email": fields.String, "role": fields.String,
              "approved": fields.Boolean(attribute='status'),
              "subject_id": fields.Integer,
              "subject_name": fields.String(attribute=lambda x: Subject_Tag.query.filter_by(subject_id=x.subject_id).first().subject_name)}

    @ jwt_required()
    @ marshal_with(output)
    def get(self):
        '''Returns a list of Staff details'''

        argument = request.args.to_dict()

        # if no query argument is passed then return all the data rows
        if len(argument) == 0:
            obj = Staff.query.all()
        elif 'status' in argument.keys():
            obj = Staff.query.filter_by(status=argument['status']).all()

        # Checking whether staff record is present
        if obj is None:
            raise DataError(status_code=404)
        return obj, 200

    @ jwt_required()
    @ marshal_with(output)
    def put(self, user_id: int):
        '''Modifies the subject_id or status for a Staff'''

        form = request.get_json()
        obj = Staff.query.filter_by(user_id=user_id).first()
        # Checking whether Staff record is present
        if not obj:
            raise DataError(status_code=404)

        # Input data checking
        if form.get('subject_id') is None and form.get('status') is None:
            raise LogicError(status_code=400, error_code='STAFF001',
                             error_msg='Tag-id must be provided')

        # checking for which operation to perform
        if form.get('subject_id'):
            if Subject_Tag.query.filter_by(subject_id=form.get('subject_id')).first():
                obj.subject_id = form.get('subject_id')
            else:
                raise LogicError(status_code=400, error_code='STAFF002',
                                 error_msg='Valid Subject-id is required')
        if form.get('status') is not None:
            obj.status = form.get('status')

        db.session.commit()
        return obj, 202

    @ jwt_required()
    def delete(self, user_id: int):
        '''Removes a Staff details'''

        obj = Staff.query.filter_by(user_id=user_id).first()

        # Checking whether Staff record is present
        if not obj:
            raise DataError(status_code=404)

        db.session.delete(obj)
        db.session.commit()
        return '', 200
