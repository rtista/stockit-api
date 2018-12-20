# Imports
from models import Warehouse, UserWarehouse, AuthToken

# Batteries
from time import time

# Third party imports
import falcon
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError, NoReferenceError


class WarehouseResource:

    def on_get(self, req, resp):
        """
        Returns warehouse in the user account.

        Args:
            req ([type]): The request object.
            resp ([type]): The response object.
        """
        # TODO: Create Hook to handle this common necessity
        # Read Authorization header
        if req.auth == None:
            raise falcon.HTTPBadRequest('Bad Request', 'No Authorization header provided.')

        # Index 0: Authentication Type
        # Index 1: Token
        auth = req.auth.split(' ')

        # Get user_id from valid token and auth_type
        token = self.db_conn.query(AuthToken).filter(AuthToken.auth_type == auth[0],
         AuthToken.token == auth[1], AuthToken.expires_at > int(time())).first()

        # Check if token exists
        if token == None:
            raise falcon.HTTPUnauthorized('Unauthorized', 'Invalid authentication token.')

        warehouses = []

        for warehouse in self.db_conn.query(Warehouse).filter(UserWarehouse.user_id == token.user_id).join(UserWarehouse, UserWarehouse.warehouse_id == Warehouse.warehouse_id):
            warehouses.append({'name': warehouse.name, 'description': warehouse.description})

        resp.media = {'warehouses': warehouses}
        resp.status = falcon.HTTP_200


    def on_post(self, req, resp):
        """
        Handle POST requests.
        """
        # Read Authorization header
        if req.auth == None:
            raise falcon.HTTPBadRequest('Bad Request', 'No Authorization header provided.')

        # Index 0: Authentication Type
        # Index 1: Token
        auth = req.auth.split(' ')

        # Get user_id from valid token and auth_type
        token = self.db_conn.query(AuthToken).filter(AuthToken.auth_type == auth[0],
         AuthToken.token == auth[1], AuthToken.expires_at > int(time())).first()

        # Check if token exists
        if token == None:
            raise falcon.HTTPUnauthorized('Unauthorized', 'Invalid authentication token.')

        # Read warehouse details
        name = req.media.get('name')
        description = req.media.get('description')
        latitude = req.media.get('latitude')
        longitude = req.media.get('longitude')

        # Check if parameters not empty
        if None in [name, description]:
            raise falcon.HTTPBadRequest('Bad Request', 'Invalid Parameters')

        # Create warehouse
        warehouse = Warehouse(name=name, description=description, latitude=latitude, longitude=longitude)

        self.db_conn.add(warehouse)

        # Attempt database changes commit
        try:
            # Create warehouse
            self.db_conn.commit()
            
            user_warehouse = UserWarehouse(warehouse_id=warehouse.warehouse_id, user_id=token.user_id, permission='rw')

            self.db_conn.add(user_warehouse)

            self.db_conn.commit()

        except SQLAlchemyError as e:

            # Rollback Changes
            self.db_conn.rollback()

            # Send error
            print('Message: {}'.format(str(e)))
            raise falcon.HTTPInternalServerError('Internal Server Error', 'Message: {}'.format(str(e)))

        resp.media = {'success': 'Warehouse created successfuly'}
        resp.status = falcon.HTTP_201
