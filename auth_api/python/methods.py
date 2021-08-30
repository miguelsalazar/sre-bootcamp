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

    def access_data(self, authorization):
        return 'test'
