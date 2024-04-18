import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    def get_id(self):
        return self.user_id


class Staff(User):
    __tablename__ = 'Staff'
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"),
                        nullable=False, primary_key=True)
    status = db.Column(db.Boolean, default=False, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("Subject_Tag.subject_id"),
                           nullable=False)


class Subject_Tag(db.Model):
    __tablename__ = "Subject_Tag"
    subject_id = db.Column(db.Integer, nullable=False,
                           primary_key=True, autoincrement=True)
    subject_name = db.Column(db.String, nullable=False, unique=True)
    ticket_list = db.relationship('Ticket', cascade="delete")


class Secondary_Tag(db.Model):
    __tablename__ = "Secondary_Tag"
    sec_tag_id = db.Column(db.Integer, nullable=False,
                           primary_key=True, autoincrement=True)
    sec_tag_name = db.Column(db.String, nullable=False, unique=True)


class Ticket(db.Model):
    __tablename__ = 'Ticket'
    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"),
                        nullable=False)
    title = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    isFAQ = db.Column(db.Boolean, nullable=False, default=False)
    ticket_status = db.Column(db.String, nullable=False, default='unresolved')
    likes = db.relationship("Table_likes", cascade='delete')
    subject_id = db.Column(db.String, db.ForeignKey('Subject_Tag.subject_id'),
                           nullable=False)
    sec_id = db.Column(db.String,
                       db.ForeignKey('Secondary_Tag.sec_tag_id'))
    timecreation = db.Column(db.DateTime, default=datetime.datetime.now)
    response_list = db.relationship("Response", cascade="delete")


class Table_likes(db.Model):
    __tablename__ = 'Table_likes'
    ticket_id = db.Column(db.Integer, db.ForeignKey("Ticket.ticket_id"),
                          primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"),
                        primary_key=True, nullable=False)


'''
class Tag_relation(db.Model):
    __tablename__ = 'Tag_relation'
    tag_id = db.Column(db.Integer, db.ForeignKey("Tag.tag_id"),
                       primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("Ticket.ticket_id"),
                          primary_key=True)
'''


class Response(db.Model):
    __tablename__ = 'Response'
    response_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey(
        "Ticket.ticket_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "User.user_id"), nullable=False)
    response = db.Column(db.String, nullable=False)
    isAnswer = db.Column(db.Boolean, nullable=False, default=False)
