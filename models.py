from app import db, ma
from sqlalchemy.orm import relationship
from datetime import datetime



class User(db.Model):
    __tablename__ = 'users'
    
    uid = db.Column(db.Integer, primary_key=True,autoincrement=True )
    uname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('uid', 'uname', 'email','password')

user_schema = UserSchema(many=False)
user_schema = UserSchema(many=True)



class Role(db.Model):
    __tablename__ = 'roles'
    
    role_id = db.Column(db.Integer, primary_key=True)
    rname = db.Column(db.String(100), unique=True, nullable=False)


class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, autoincrement=True, nullable=False)
    # aemail = db.column(db.Integer,nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), default=1)
    role = db.relationship('Role', backref=db.backref('admin', lazy=True))

class AdminSchema(ma.Schema):
    class Meta:
        fields = ('admin_id','password','role_id','role')

admin_schema = AdminSchema(many=False)
admin_schema = AdminSchema(many=True)


class Course(db.Model):
    __tablename__ = 'courses'

    cid = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500),nullable=False)
    fee = db.Column(db.String(100))
    ctime = db.Column(db.String(100),nullable=True)
    rating = db.Column(db.Float,nullable=False)
    lessons = relationship('Lesson', back_populates='course', cascade='all, delete-orphan')
    assignment = db.relationship('Assignment', back_populates='course', cascade='all, delete-orphan')
    # quiz = db.relationship('Quiz', back_populates='mycourse', cascade='all, delete-orphan')
    quizzes = relationship('Quiz', back_populates='mycourse', primaryjoin="Course.cid == Quiz.cid")


    def serialize(self):
        return {
            'cid': self.cid,
            'cname': self.cname,
            'description': self.description,
            'fee': self.fee,
            'ctime':self.ctime,
            'rating':self.rating,
            'lessons': [lesson.serialize() for lesson in self.lessons]
        }


class CourseSchema(ma.Schema):
    class Meta:
        fields = ('cid', 'cname', 'description', 'fee', 'ctime','rating')

course_schema = CourseSchema(many=False)
course_schema = CourseSchema(many=True)



class Lesson(db.Model):
    __tablename__ = 'lessons'

    lid = db.Column(db.Integer, primary_key=True)
    l_id = db.Column(db.Integer)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('courses.cid'))
    course = db.relationship('Course', back_populates='lessons')
    # quiz = db.relationship('Quiz', back_populates='mylesson', cascade='all, delete-orphan')

    def serialize(self):
        return {
            'l_id': self.l_id,
            'title': self.title,
            'content': self.content,
        }


class Enroll(db.Model):
    __tablename__ = 'enrolls'

    eid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    epassword = db.Column(db.String(500),nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('courses.cid'), nullable=False)
    etime = db.Column(db.DateTime)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), default=2)  
    role = db.relationship('Role', backref=db.backref('enrolls', lazy=True))
    course = db.relationship('Course',backref=db.backref('courses',lazy=True))
    user = db.relationship('User',backref=db.backref('users',lazy=True))


class Progress(db.Model):
    __tablename__ = 'progress'

    sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer,db.ForeignKey('users.uid'),nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    cid = db.Column(db.Integer, db.ForeignKey('courses.cid'),nullable=False)
    lesson_completed = db.Column(db.Integer,nullable=False)
    myprogress = db.Column(db.String,nullable=False)
    eid = db.Column(db.Integer, db.ForeignKey('enrolls.eid'),nullable=True)
    course = db.relationship('Course',backref=db.backref('progresses',lazy=True))
    user = db.relationship('User',backref=db.backref('progresses',lazy=True))
    enroll = db.relationship('Enroll',backref=db.backref('progresses',lazy=True))


class Assignment(db.Model):
    __tablename__ = 'assignment'

    aid = db.Column(db.Integer,primary_key=True, autoincrement=True)
    qid = db.Column(db.Integer)
    question = db.Column(db.Text, nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('courses.cid'),nullable=False)
    # course = db.relationship('Course',backref=db.backref('mycourse',lazy=True))
    course = relationship('Course', back_populates='assignment')

    def serialize(self):
        return {
            'qid': self.qid,
            'question': self.question,
            'course': self.course.cname,  
        }


class Quiz(db.Model):
    __tablename__ = 'quiz'

    quiz_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    q_id = db.Column(db.Integer)
    qcontent = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text, nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('courses.cid'),nullable=False)
    l_id = db.Column(db.Integer, nullable=False)
    mycourse = relationship('Course', back_populates='quizzes')

    def serialize(self):
        return {
            'q_id': self.q_id,
            'qcontent': self.qcontent,
            'options': self.options,
            'mycourse': self.mycourse.cname,
            'l_id':self.l_id
        }