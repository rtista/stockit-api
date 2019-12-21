# Imports
from models import User

# Third party imports
import falcon
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError, NoReferenceError


class UserResource:

    def on_get(self, req, resp):
        """
        Returns users in an account.

        Args:
            req ([type]): The request object.
            resp ([type]): The response object.
            account_id ([type]): The account_id.
        """
        users = []

        for user in self.db_conn.query(User):
            users.append({
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
            })

        resp.media = {
            'users': users
        }
        resp.status = falcon.HTTP_200


    def on_post(self, req, resp):
        """
        Handle POST requests.
        """
        username = req.media.get('username')
        password = req.media.get('password')
        email = req.media.get('email')

        # Check if parameters not empty
        if None in [username, password, email]:
            raise falcon.HTTPBadRequest('Bad Request', 'Invalid Parameters')

        # Hash user password
        hashed = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
        
        # Now create main user for account
        user = User(username=username, password=hashed, email=email)

        self.db_conn.add(user)

        # Attempt database changes commit
        try:
            # Create Account
            self.db_conn.commit()

        except SQLAlchemyError as e:

            # Rollback Changes
            self.db_conn.rollback()

            # Send error
            print('Message: {}'.format(str(e)))
            raise falcon.HTTPInternalServerError('Internal Server Error', 'Message: {}'.format(str(e)))
        
        resp.media = {'success': 'User created successfuly'}
        resp.status = falcon.HTTP_201
