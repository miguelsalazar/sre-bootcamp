from flask import Flask
from flask import jsonify
from flask import request
from methods import Token, Restricted
from os import environ
from flask_mysqldb import MySQL
import hashlib
import jwt

app = Flask(__name__)
login = Token()
protected = Restricted()

app.config['MYSQL_USER'] = environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = environ.get("MYSQL_PASSWORD")
app.config['MYSQL_HOST'] = environ.get("MYSQL_HOST")
app.config['MYSQL_DB'] = environ.get("MYSQL_DB")
app.config['MYSQL_PORT'] = int(environ.get("MYSQL_PORT"))
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

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

    cur = mysql.connection.cursor()
    query = f"SELECT * FROM users WHERE username='{username}';"
    cur.execute(query)
    results = cur.fetchall()

    salt = results[0]['salt']
    salted_input = str(password + salt).encode('utf-8')
    h = hashlib.sha512()
    h.update(salted_input)
    hashed_password = h.hexdigest()
    db_password = results[0]['password']    
    role = results[0]['role']

    res = {}
    if hashed_password == db_password:
        res = {
            "data": login.generate_token(role)
        }

    return jsonify(res)


# # e.g. http://127.0.0.1:8000/protected
@app.route("/protected")
def url_protected():
    auth_header = request.headers.get('Authorization')
    auth_token = auth_header.split(" ")[1]
    res = {
        "data": protected.access_data(auth_token)
    }
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
