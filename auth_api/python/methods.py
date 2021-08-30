import jwt 
from os import environ

# These functions need to be implemented
class Token:

    def generate_token(self, role):
        
        payload = {
            'role': role
        }
        return jwt.encode(
                payload,
                environ.get('JWT_SECRET_KEY'),
                algorithm='HS256'
        )


class Restricted:

    def access_data(self, auth_token):
        data = ""
        try:
            payload = jwt.decode(
                auth_token, 
                environ.get('JWT_SECRET_KEY'),
                algorithms=['HS256']
            )
            if payload:
                data = 'You are under protected data'
            return data

        except jwt.InvalidTokenError:
            data = 'Invalid token.'
            return data
        
        except Exception:
            return data
