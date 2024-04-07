from marshmallow import Schema, fields, validate, ValidationError 
import re


class UsernameValidator:
    @staticmethod
    def validate_name(uname):
        if uname[0].islower():
            raise ValidationError("Username must start with a capital letter")


class EmailValidator:
    @staticmethod
    def validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError('Invalid email address')


class PasswordValidator:
    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long')

        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter')

        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one digit')

        if not re.search(r'[\W]', password):
            raise ValidationError('Password must contain at least one special character')


class UserSchema(Schema):
    uid = fields.Integer(required = True)
    uname = fields.String(required=True, validate=[UsernameValidator.validate_name, validate.Length(min=1, max=100)])
    email = fields.Email(required=True, validate=EmailValidator.validate_email)
    password = fields.String(required=True, validate=PasswordValidator.validate_password)


class RoleSchema(Schema):
    role_id = fields.Integer(dump_only=True)
    rname = fields.String(required=True, validate=validate.Length(min=1, max=100))


class AdminSchema(Schema):
    id = fields.Integer(dump_only=True)
    admin_id = fields.Integer(required=True, validate=validate.Range(min=1))
    role_id = fields.Integer(default=1)


class CourseSchema(Schema):
    cid = fields.Integer(required=True)
    cname = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description =fields.String(required=True, validate=validate.Length(min=1,max=500))
    fee = fields.String(validate=validate.Length(min=1, max=100))
    ctime = fields.String(allow_none=True,validate=validate.Length(min=1, max=100))
    rating = fields.Float(required=True)


class LessonSchema(Schema):
    lid = fields.Integer(requird=True)
    l_id = fields.Integer(required=True)
    title = fields.String(requird=True, validate=validate.Length(min=1,max=200))
    content = fields.String(required=True)
    cid = fields.Integer()


class EnrollSchema(Schema):
    eid = fields.Integer(dump_only=True)
    uid = fields.Integer(required=True)
    epassword = fields.String(required=True,validate=validate.Length(min=1,max=100))
    cid = fields.Integer(required=True)
    etime = fields.DateTime()
    role_id = fields.Integer(default=2)


class Progress(Schema):
    sid = fields.Integer(dump_only=True)
    uid = fields.Integer(required=True)
    cid = fields.Integer(required=True)
    lesson_completed = fields.Integer(required=True)
    myprogress = fields.String(required=True,validate=validate.Length(min=1,max=100))
    eid = fields.Integer(required=True)


class AssignmentSchema(Schema):
    aid = fields.Integer(dump_only=True)
    qid = fields.Integer(required=True)
    question = fields.String(required=True)
    cid = fields.Integer()





