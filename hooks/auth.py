# Own imports
from models import AuthToken

# Batteries
from time import time

# Third-party imports
import falcon

class Authorize(object):

    def __call__(self, req, resp, resource, params):
        """
        Associate user_id with the resource object.
        
        Reads the Authorization header from the request, 
        validating its syntax and and expiration. If
        everything checks out it will append the 'user_id'
        to the resource object.
        
        Args:
            req ([type]): [description]
            resp ([type]): [description]
            resource ([type]): [description]
            params ([type]): [description]
        
        Raises:
            falcon.HTTPBadRequest: On missing authorization header.
            falcon.HTTPUnauthorized: On invalid token.
        """

        # Read Authorization header and check syntax
        if req.auth == None or ' ' not in req.auth:
            raise falcon.HTTPBadRequest('Bad Request', 'No Authorization header provided.')

        # Index 0: Authentication Type
        # Index 1: Token
        auth = req.auth.split(' ')

        # Get user_id from valid token and auth_type
        token = resource.db_conn.query(AuthToken).filter(AuthToken.auth_type == auth[0],
         AuthToken.token == auth[1:], AuthToken.expires_at > int(time())).first()

        # Check if token exists
        if token == None:
            raise falcon.HTTPUnauthorized('Unauthorized', 'Invalid authentication token.')

        # On success add token to resource object
        resource.user_id = token.user_id