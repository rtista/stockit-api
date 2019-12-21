# Imports
from models import Account, User

# Third party imports
import falcon
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError


class AccountResource:

    def on_post(self, req, resp):
        """
        Handle POST requests.
        """
        account_name = req.media.get('name')
        username = req.media.get('username')
        password = req.media.get('password')

        # Check if parameters not empty
        if None in [account_name, username, password]:
            resp.media = {'error': 'Invalid Parameters'}
            resp.status_code = falcon.HTTP_400
            return

        # Hash user password
        hashed = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
        
        account = Account(name=account_name)

        self.db_conn.add(account)

        # Attempt database changes commit
        try:
            # Create Account
            self.db_conn.commit()

            # Now create main user for account
            user = User(account_id=account.account_id, username=username, password=hashed)

            self.db_conn.add(user)

            self.db_conn.commit()

        except SQLAlchemyError as e:

            # Remove Changes
            self.db_conn.rollback()

            # Send error
            resp.media = {'error': 'Message: {}'.format(str(e))}
            resp.status_code = falcon.HTTP_500
            return
        
        resp.media = {'success': 'Account created successfuly'}
        resp.status_code = falcon.HTTP_201