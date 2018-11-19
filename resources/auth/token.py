# Imports
from models import User

# Third party imports
import falcon
from passlib.hash import pbkdf2_sha256


class AuthTokenResource:

    def on_post(self, req, resp):
        """
        Handle POST requests.
        """
        username = req.media.get('username')
        password = req.media.get('password')

        # Check if parameters not empty
        if None in [username, password]:
            resp.media = {'error': 'Invalid Parameters'}
            resp.status_code = falcon.HTTP_400
            return

        user = self.db_conn.query(User).filter_by(username=username).first()

        # If user does not exist
        if user == None:
            resp.media = {'error': 'Wrong credentials'}
            resp.status_code = falcon.HTTP_401
            return

        # If passowrd does not match
        if not pbkdf2_sha256.verify(password, user.password):
            resp.media = {'error': 'Wrong credentials'}
            resp.status_code = falcon.HTTP_401
            return

        # TODO Create user token (memory sqlite?)

        resp.media = {'token': 'haveatoken'}
        resp.status_code = falcon.HTTP_201
