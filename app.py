from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_swagger_ui import get_swaggerui_blueprint
from flask_marshmallow import Marshmallow


app=Flask(__name__)

app.config['SECRET_KEY'] = "this is secret"
	
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1719@localhost:5432/mydata'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Course Management System",
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app,db)


@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)



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
