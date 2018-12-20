# Imports
from models import User, AuthToken
from config import AppConfig

# Batteries
from time import time

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
            raise falcon.HTTPBadRequest('Bad Request', 'Invalid Parameters')

        user = self.db_conn.query(User).filter_by(username=username).first()

        # If user does not exist
        if user == None:
            raise falcon.HTTPUnauthorized('Unauthorized', 'Wrong Credentials')

        # If password does not match
        if not pbkdf2_sha256.verify(password, user.password):
            raise falcon.HTTPUnauthorized('Unauthorized', 'Wrong Credentials')

        # Get user bearer token
        token = self.db_conn.query(AuthToken).filter_by(user_id=user.user_id).first()

        # Check if user does not have token
        if token == None:

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

        # If user has token but it has expired
        elif token.expires_at < time():

            # Create user token (32 bits length)
            cond = False
            
            while not cond:
                token.token = token_hex(16)
                token.expires_at = time() + AppConfig.TOKEN_LIFE

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
        resp.status = falcon.HTTP_201
