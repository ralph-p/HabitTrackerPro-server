from flask import Flask, Response, jsonify, json, request
from sb_controller import find_all_profiles, login_user, get_user, get_task_list
from utils import get_token
application = Flask(__name__)

@application.route('/')
def hello_world():
    return jsonify({
        'greeting': 'Welcome to Habit Tracker Pro'
    })
@application.route('/login',  methods=['POST'])
def login():
    data = request.get_json()
    try:
        email = data['email']
        password = data['password']
        return jsonify({
            'session': login_user(email, password),
        }, 201)
    except Exception as e:
        print(e)
        return Response('''{"message": "Bad Request"}''', status=400, mimetype='applicationlication/json')

@application.route('/user')
def user():
    token = get_token(request)
    return jsonify({
        'user': get_user(token),
    })

@application.route('/profiles')
def profiles():
    return jsonify({
        'profiles': find_all_profiles(),
    })

@application.route('/tasks')
def tasks():
    token = get_token(request)
    return jsonify({
        'tasks': get_task_list(token),
    })
if __name__ == '__main__':
    application.run(host='0.0.0.0', debug = True)