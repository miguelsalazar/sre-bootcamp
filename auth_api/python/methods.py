from os import environ
import hashlib
from mysql.connector import connect, Error
import jwt 

# These functions need to be implemented
class Token:

    def __init__(self, db):
        self.db = db

    def connect_to_db(self): 
        conn = connect(
                user = self.db['user'],
                password = self.db['password'],
                database = self.db['database'],
                host = self.db['host'],
                port = int(self.db['port'])
        )
        return conn

    def query_user_data(self, connection, username):
        cursor = connection.cursor()
        query = f"SELECT * FROM users WHERE username='{username}';"
        cursor.execute(query)
        result = cursor.fetchall()
        user = {
            'user': result[0][0],
            'password': result[0][1],
            'salt': result[0][2],
            'role': result[0][3]
        }
        return user
    
    def hash_password(self, salt, password):
        salted_input = str(password + salt).encode()
        h = hashlib.sha512()
        h.update(salted_input)
        hashed_password = h.hexdigest()
        return hashed_password

    def generate_token(self, username, password):
        connection = self.connect_to_db()
        user = self.query_user_data(connection, username)
        hashed_password = self.hash_password(user['salt'], password)
        db_password = user['password'] 
        if hashed_password == db_password:
            try: 
                payload = {
                    "role": user['role']
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

            

