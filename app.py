from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

app=Flask(__name__)

app.config['SECRET_KEY'] = "this is secret"
	
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1719@localhost:5432/mydata'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


migrate = Migrate(app,db)


from routes import auth
app.register_blueprint(auth)

from course import mycourse
app.register_blueprint(mycourse)

from lesson import mylesson
app.register_blueprint(mylesson)

from enroll import enrolled
app.register_blueprint(enrolled)

from student import student_track
app.register_blueprint(student_track)


if __name__ == '__main__':
    app.run(debug=True)
