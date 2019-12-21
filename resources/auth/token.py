# Imports
from models import User, AuthToken
from config import AppConfig
from hooks import Authorize

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

    @falcon.before(Authorize())
    def on_delete(self, req, resp):
        """
        Handles DELETE requests.
        
        Allows deleting user authentication bearer tokens.
        
        Args:
            req ([type]): The request object.
            resp ([type]): The response object.
        """
        # Get token by user id
        self.db_conn.query(AuthToken).filter_by(user_id=self.user_id).delete()

        # Commit modifications
        try:
            self.db_conn.commit()

        except Exception:

            # Rollback Changes
            self.db_conn.rollback()
            raise falcon.HTTPInternalServerError('Internal Server Error', 'An error ocurred, please inform the development team.')

        resp.media = {'success': 'User authentication token deleted successfuly'}
        resp.status = falcon.HTTP_200