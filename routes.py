from flask import Blueprint
import jwt 
from app import app,db
# from app import db
from models import User,Course,Admin
from flask_bcrypt import  generate_password_hash
from flask_bcrypt import check_password_hash
from datetime import datetime
from datetime import datetime, timedelta
from flask import request,jsonify, Blueprint 
from flask_bcrypt import bcrypt 
from flask_bcrypt import Bcrypt 
from validation import *


bcrypt = Bcrypt(app)

auth=Blueprint('auth',__name__)

@auth.route('/user/signup',methods=['POST'])
def signup():
    user_schema = UserSchema()
    try:
        validated_data = user_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400
    existing_user = User.query.filter_by(uid=validated_data['uid']).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400
    hashed_password = bcrypt.generate_password_hash(validated_data['password']).decode('utf-8')
    new_user = User(uid=validated_data['uid'],uname=validated_data['uname'], email=validated_data['email'], 
                    password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'Register Successfully'}), 201

    
@auth.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    uid = data.get("uid")
    password = data.get("password")
    user = User.query.filter_by(uid=uid).first()
    if user:
        if bcrypt.check_password_hash(user.password, password):
            courses = Course.query.all()
            serialized_courses = []
            for course in courses:
                serialized_course = course.serialize()
                serialized_course['lessons'] = [lesson.serialize() for lesson in course.lessons]
                serialized_courses.append(serialized_course)
            return jsonify(serialized_courses)             
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    else:
        return jsonify({'error': 'User not found'}), 404

            
@auth.route('/dashboard/user', methods=['GET'])
def dashboard_user():
    users = User.query.all()
    output = []
    for u in users:
        udata = {
            'uid': u.uid,
            'uname': u.uname,
            'email': u.email,
            'password': u.password
        }
        output.append(udata)
    return jsonify(output)

@auth.route('/create/admin', methods=['POST'])
def create_admin():
    data = request.get_json()
    admin_id = data.get("admin_id")
    password = data.get("password")
    role_id = data.get("role_id")
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_admin = Admin(admin_id=admin_id, password=hashed_password, role_id=role_id)
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'message': 'Admin created successfully'}), 201        

@auth.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin_id = data.get("admin_id")
    password = data.get("password")
    admin = Admin.query.filter_by(admin_id=admin_id).first()
    if admin:
        hashed_password = admin.password
        if bcrypt.check_password_hash(hashed_password, password):
            token = jwt.encode({
                'admin_id': admin.admin_id,
                'role_id': admin.role_id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({'token': token}), 201
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    else:
        return jsonify({'error': 'Admin not found'}), 404
    

@auth.route('/dashboard/admin', methods=['GET'])
def dashboard_admin():
    admin = Admin.query.all()
    output = []
    for a in admin:
        adata = {
            'admin_id': a.admin_id,
            'password': a.password,
            'role_id':a.role_id
        }
        output.append(adata)
    return jsonify(output)
