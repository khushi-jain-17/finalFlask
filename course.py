from flask import request,jsonify,Blueprint
from myrole import *
from app import db
from models import Course
import logging

mycourse = Blueprint('mycourse',__name__)


@mycourse.route("/create/course", methods=['POST'])
@token_required
def create():
    cid = request.json["cid"]
    cname = request.json["cname"]
    description = request.json["description"]
    fee = request.json["fee"]
    ctime = request.json["ctime"]
    rating = request.json["rating"]
    new_course = Course(cid=cid,cname=cname,description=description,fee=fee,ctime=ctime,rating=rating)
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'message': 'course created successfully'}), 201


@mycourse.route('/courses', methods=['GET'])
@token_required
def get_courses():
    try:
        course = Course.query.all()
        output = []
        for c in course:
            course_data = {
                'cid': c.cid,
                'cname': c.cname,
                'description': c.description,
                'fee': c.fee,
                'ctime': c.ctime,
                'rating': c.rating
            }
            output.append(course_data)
        return jsonify(output), 200  # 200 OK
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # 500 Internal Server Error


@mycourse.route('/course/<int:cid>',methods=['GET'])
@token_required
def getbyid(cid):
    course = Course.query.get_or_404(cid)
    output=[]
    cdata = {
        'cname': course.cname,
        'description': course.description,
        'fee':course.fee,
        'ctime':course.ctime,
        'rating':course.rating
    }
    output.append(cdata)
    return jsonify({'course':output})


@mycourse.route("/update_course/<int:cid>",methods=['PUT'])
@token_required
def update(cid):
    course = Course.query.get_or_404(cid)
    data = request.get_json()
    course.cname = data.get("cname")
    course.description = data.get("description")
    course.fee = data.get("fee")
    course.ctime = data.get("ctime")
    course.rating = data.get("rating")
    db.session.commit()
    return jsonify({'message':'Course Updated Successfully'})


@mycourse.route("/delete_course/<int:cid>", methods=['DELETE'])
@token_required
def delete(cid):
    course = Course.query.get_or_404(cid)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course Deleted Successfully'})


@mycourse.route('/course/<int:cid>', methods=['GET'])
@token_required
def course_analytics(cid):
    course = Course.query.get(cid)
    if course:
        return jsonify(course.serialize())
    else:
        return jsonify({'error': 'Course not found'}), 404
    

@mycourse.route('/courses/lessons', methods=['GET'])
@token_required
def courseAnalytics():
    courses = Course.query.all()
    serialized_courses = []
    for course in courses:
        serialized_course = course.serialize()
        serialized_course['lessons'] = [lesson.serialize() for lesson in course.lessons]
        serialized_courses.append(serialized_course)
    return jsonify(serialized_courses)


@mycourse.route('/dashboard/course', methods=['GET'])
@token_required
def dashboard():
    course = Course.query.all()
    output = []
    for c in course:
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


@mycourse.route("/course/paginate", methods=['GET'])
@token_required
def paginate():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 2, type=int)
    course = Course.query.paginate(
        page=page, per_page=per_page, error_out=True
    )
    output = []
    for c in course:
        cdata = {
            "cid": c.cid,
            'cname': c.cname,
            'description':c.description,
            'fee':c.fee,
            'ctime':c.ctime,
            'rating':c.rating
        }
        output.append(cdata)
    return jsonify({"course": output})