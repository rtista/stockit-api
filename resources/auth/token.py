# Imports
from models import User, AuthToken

# Third party imports
import falcon
from secrets import token_hex
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

        # Create user token (32 bits length)
        cond = False

        # Retry while token has not been inserted
        while not cond:
            token = AuthToken(user_id=user.user_id, auth_type='bearer', token=token_hex(16))

            try:
                self.db_conn.add(token)
                self.db_conn.commit()
                cond = True

            except Exception:
                pass

        resp.media = {
            'auth_type': token.auth_type,
            'token': token.token,
            'expires_on': token.expires_at
        }
        resp.status_code = falcon.HTTP_201
