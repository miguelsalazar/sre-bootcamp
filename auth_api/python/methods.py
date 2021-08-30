import jwt 
from os import environ

# These functions need to be implemented
class Token:

    def generate_token(self, role):
        try: 
            payload = {
                'role': role
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

            

