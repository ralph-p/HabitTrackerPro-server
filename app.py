from flask import Flask, Response, jsonify, json, request
from sb_controller import find_all_profiles, login_user, get_user, get_task_list, get_task
from utils import get_token
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return jsonify({
        'greeting': 'Welcome to Habit Tracker Pro'
    })
@app.route('/login',  methods=['POST'])
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
        return Response('''{"message": "Bad Request"}''', status=400, mimetype='application/json')

@app.route('/user')
def user():
    token = get_token(request)
    try:
        return jsonify({
            'user': get_user(token),
        })
    except Exception as e:
        print(e)
        return Response('''{"message": "Bad Request"}''', status=400, mimetype='application/json')

@app.route('/profiles')
def profiles():
    try:
        return jsonify({
            'profiles': find_all_profiles(),
        })
    except Exception as e:
        print(e)
        return Response('''{"message": "Bad Request"}''', status=400, mimetype='application/json')

@app.route('/tasks')
def tasks():
    try:
        token = get_token(request)
        return jsonify({
            'tasks': get_task_list(token),
        })
    except Exception as e:
        print(e)
        return Response('''{"message": "Bad Request"}''', status=400, mimetype='application/json')

@app.route('/task')
def task():
    try:
        token = get_token(request)
        task_id = request.args.get('task_id')
        return jsonify({
            'task': get_task(token, task_id),
        })
    except Exception as e:
        print(e)
        return Response('''{"message": "Bad Request"}''', status=400, mimetype='application/json')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)