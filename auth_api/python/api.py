from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from methods import Token, Restricted
from os import environ

app = Flask(__name__)
login = Token(app)
protected = Restricted()

app.config['MYSQL_USER'] = environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = environ.get("MYSQL_PASSWORD")
app.config['MYSQL_HOST'] = environ.get("MYSQL_HOST")
app.config['MYSQL_DB'] = environ.get("MYSQL_DB")
app.config['MYSQL_PORT'] = int(environ.get("MYSQL_PORT"))
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Just a health check
@app.route("/")
def url_root():
    return "OK"


# Just a health check
@app.route("/_health")
def url_health():
    return "OK"


# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['POST'])
def url_login():
    username = request.form['username']
    password = request.form['password']
    res = {
        "data": login.generate_token(username, password)
    }
    if res['data']:
        return jsonify(res)
    else:
        abort(403)


# # e.g. http://127.0.0.1:8000/protected
@app.route("/protected")
def url_protected():
    auth_header = request.headers.get('Authorization')
    auth_token = auth_header.split(" ")[1]
    res = {
        "data": protected.access_data(auth_token)
    }
    print(res)
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
