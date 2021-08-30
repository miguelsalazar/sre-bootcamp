from os import environ
import hashlib
from flask_mysqldb import MySQL
import jwt 
from flask import current_app

# These functions need to be implemented
class Token:

    def __init__(self, app):
        self.mysql = MySQL(app)

    def connect_to_db(self):
        cur = self.mysql.connection.cursor()
        return cur
    
    def query_user_data(self, cur, username):
        query = f"SELECT * FROM users WHERE username='{username}';"
        cur.execute(query)
        results = cur.fetchall()
        return results[0]
    
    def hash_password(self, salt, password):
        salted_input = str(password + salt).encode('utf-8')
        h = hashlib.sha512()
        h.update(salted_input)
        hashed_password = h.hexdigest()
        return hashed_password

    def generate_token(self, username, password):
        cur = self.connect_to_db()
        user = self.query_user_data(cur, username)
        
        hashed_password = self.hash_password(user['salt'], password)
        db_password = user['password'] 

        if hashed_password == db_password:
            try: 
                payload = {
                    'role': user['role']
                }
                return jwt.encode(
                        payload,
                        environ.get('JWT_SECRET_KEY'),
                        algorithm='HS256'
                )
            except Exception as e:
                return e 


class Restricted:

    def access_data(self, authorization):
        data = ''
        try:
            payload = jwt.decode(
                authorization, 
                environ.get("JWT_SECRET_KEY"), 
                algorithms=["HS256"]
            )
            if payload:
                data = 'You are under protected data'
        except jwt.InvalidTokenError:
            data = 'Error: Invalid token.'
        except Exception as e:
            data = e
        return data 

            

