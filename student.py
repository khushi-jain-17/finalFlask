from flask import request,jsonify,Blueprint
from myrole import *
from app import db
from models import Enroll,Progress,Course,User,Assignment, Quiz
from datetime import datetime


student_track = Blueprint("student_track",__name__)


@student_track.route('/progress/track',methods=['POST'])
def progress():
    data = request.get_json()
    uid = data.get("uid")
    cid = data.get("cid")
    lesson_completed = data.get("lesson_completed")
    eid = db.session.query(Enroll.eid).filter(Enroll.uid==uid).first()
    id = eid[0]
    print(id)
    lessons = 5
    total = (lesson_completed / lessons) * 100
    myprogress = f"{total}%"
    old_progress = Progress.query.filter_by(uid=uid).first()
    if old_progress:
        db.session.delete(old_progress)
        db.session.commit()
    elif not old_progress:    
        progress = Progress(uid=uid, cid=cid, eid=id, lesson_completed=lesson_completed, myprogress=myprogress)
        db.session.add(progress)
        db.session.commit()
    return jsonify({"message": "Progress recorded successfully"}), 201


@student_track.route('/dashboard/progress',methods=['GET'])
@role_required(1)
def progress_dashboard():
    query = db.session.query(
        Progress.lesson_completed,
        Progress.myprogress,
        Enroll.eid,
        Enroll.etime,
        User.uname,
        Course.cname
    ).join(
        Course,Progress.cid == Course.cid
    ).join(
        User, Progress.uid == User.uid
    ).join(
        Enroll, Progress.eid == Enroll.eid
    )
    results = query.all()
    output = []
    for result in results:
        output.append({
            'lesson_completed': result[0],
            'progess': result[1],
            'eid': result[2],
            'etime': result[3],
            'user_name': result[4],
            'course_name': result[5],
        })
    return jsonify(output), 200


@student_track.route("/create/assignment", methods=['POST'])
@role_required(1)
def create():
    qid = request.json["qid"]
    question = request.json["question"]
    cid = request.json["cid"]
    adata = Assignment(qid=qid,question=question,cid=cid)
    db.session.add(adata)
    db.session.commit()
    return jsonify({'message': 'Assignment created successfully'}), 201
    
 
@student_track.route('/eligibility', methods=['GET'])
@role_required(2)
def CheckEligibility():
    data = request.get_json()
    uid = data.get("uid")
    cid = data.get("cid")
    assignments = Assignment.query.filter_by(cid=cid).all()
    serialized_assignments = [assignment.serialize() for assignment in assignments]
    p = Progress.query.filter_by(uid=uid, cid=cid).first()
    if not p.myprogress:
        return jsonify({"error": "Progress not found for the student in this course."}), 404
    if p.myprogress == "100.0%" :
        return jsonify({"message":"You are eligible for the assignment", "assignments":serialized_assignments}), 200
    else:
        return jsonify({"message": "Keep working! You are not eligible for the assignment yet."}), 200
    

@student_track.route('/assignments/<int:cid>', methods=['GET'])
def get_assignments_by_course(cid):
    assignments = Assignment.query.filter_by(cid=cid).all()
    serialized_assignments = [assignment.serialize() for assignment in assignments]
    return jsonify(serialized_assignments)


@student_track.route("/create/quiz", methods=['POST'])
@role_required(1)
def create_quiz():
    q_id = request.json["q_id"]
    qcontent = request.json["qcontent"]
    options = request.json["options"]
    cid = request.json["cid"]
    l_id = request.json["l_id"]
    new_quiz = Quiz(q_id=q_id,qcontent=qcontent,options=options,cid=cid,l_id=l_id)
    db.session.add(new_quiz)
    db.session.commit()
    return jsonify({'message': 'Quiz created successfully'}), 201


@student_track.route('/lessonquiz/<int:l_id>', methods=['GET'])
@role_required(2)
def lesson_analytics(l_id):
    quiz = Quiz.query.get(l_id)
    if quiz:
        return jsonify(quiz.serialize())
    else:
        return jsonify({'error': 'Lesson not found'}), 404
    

@student_track.route('/quiz', methods=['GET'])
@role_required(2) 
def quiz_by_lessons():
    lid_value = request.json["lid_value"]
    cid_value = request.json["cid_value"]
    quizzes = Quiz.query.filter(Quiz.l_id == lid_value, Quiz.cid == cid_value).all()
    serialized_quizzes = [quiz.serialize() for quiz in quizzes]
    return jsonify(serialized_quizzes)
