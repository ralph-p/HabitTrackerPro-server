from flask import Flask, Response, jsonify, json, request
from sb_controller import find_all_profiles, login_user, get_user
app = Flask(__name__)

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
        return jsonify({
            'session': login_user(email),
        }, 201)
    except Exception as e:
        print(e)
        return Response('''{"message": "Bad Request"}''', status=400, mimetype='application/json')

@app.route('/user')
def user():
    get_user()
    return jsonify({
        'user': 'bob',
    })

@app.route('/profiles')
def profiles():
    return jsonify({
        'profiles': find_all_profiles(),
    })
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)