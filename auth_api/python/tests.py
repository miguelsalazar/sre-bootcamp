import unittest
from methods import Token, Restricted
from os import environ

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        user =  environ.get("MYSQL_USER")
        password = environ.get("MYSQL_PASSWORD")
        host = environ.get("MYSQL_HOST")
        db = environ.get("MYSQL_DB")
        port = environ.get("MYSQL_PORT")
        conn = {
            'user': user,
            'password': password,
            'host': host,
            'database': db,
            'port': port
        }
        self.convert = Token(conn)
        self.validate = Restricted()

    def test_generate_token(self):
        # Couldn't reproduce original JWT
        self.assertEqual('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXOx9w', self.convert.generate_token('admin', 'secret'))

    def test_access_data(self):        
        self.assertEqual('You are under protected data', self.validate.access_data('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXOx9w'))

if __name__ == '__main__':
    unittest.main()
