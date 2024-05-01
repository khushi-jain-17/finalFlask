from flask import request,jsonify,Blueprint
from app import db
from myrole import *
from models import Enroll,User,Course
from datetime import datetime, timedelta


enrolled = Blueprint('enrolled',__name__)


@enrolled.route('/enroll/user',methods=['POST'])
def enroll_user():
    data = request.get_json()
    uid = data.get("uid")
    cid = data.get("cid")
    etime = datetime.now().strftime("%Y-%m-%dT%H:%M")
    password = db.session.query(User.password).filter(User.uid == uid).first()
    p=password[0]
    enroll_user = Enroll(uid=uid,epassword=p,cid=cid,etime=etime)
    db.session.add(enroll_user)
    db.session.commit()
    token = jwt.encode({
                'eid': enroll_user.eid,
                'role_id': enroll_user.role_id,
                 'exp': datetime.utcnow() + timedelta(days=365)
            }, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'message': 'Enrolled Successfully','token':token}), 201


@enrolled.route('/courses/search', methods=['GET'])
@role_required(2)
def search_courses():
    keyword = request.args.get('keyword')
    # keyword = request.json["keyword"]
    mycourse = Course.query
    if keyword:
        find = mycourse.filter(Course.cname.ilike(f"%{keyword}%"))
    courses = find.all()
    data = [{'cid': course.cid, 'cname': course.cname, 'description': course.description, 'fee': course.fee, 'ctime': course.ctime, 'rating': course.rating} for course in courses]
    return jsonify(data)  


@enrolled.route('/sorting',methods=['GET'])
@role_required(2)
def Top_rated_course():
    courses = Course.query.order_by(Course.rating.desc()).all()
    output = []
    for c in courses:
        course_data = {
            'cid': c.cid,
            'cname': c.cname,
            'description':c.description,
            'fee':c.fee,
            'ctime':c.ctime,
            'rating':c.rating
        }
        output.append(course_data)
    return jsonify(output)


@enrolled.route('/dashboard/student',methods=['GET'])
@role_required(1)
def enroll_dashboard():
    query = db.session.query(
        Enroll.eid,
        Enroll.etime,
        Course.cname,
        User.uid,
        User.uname,
        User.email
    ).join(
        Course, Enroll.cid == Course.cid
    ).join(
        User, Enroll.uid == User.uid
    )
    results = query.all()
    enrolled_users = []
    for result in results:
        enrolled_users.append({
            'eid': result[0],
            'etime': result[1],
            'course_name': result[2],
            'uid': result[3],
            'username': result[4],
            'email': result[5]
        })
    return jsonify(enrolled_users), 200


@enrolled.route('/update/enroll/<int:eid>',methods=['UPDATE'])
@role_required(1)
def update(eid):
    student = Enroll.query.get_or_404(eid)
    data = request.get_json()
    student.cid = data.get("cid")
    student.uid = data.get("uid")
    db.session.commit()
    return jsonify({'message':'Enrollment Updated Successfully'})


@enrolled.route('/disenroll/<int:eid>',methods=['DELETE'])
@role_required(1)
def disenroll(eid):
    student = Course.query.get_or_404(eid)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Disenrolled from Course Successfully'})

