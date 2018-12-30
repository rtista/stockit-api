# Imports
from models import Warehouse, UserWarehouse
from hooks import Authorize

# Batteries
from time import time

# Third party imports
import falcon
from sqlalchemy.exc import SQLAlchemyError, NoReferenceError

@falcon.before(Authorize())
class WarehouseResource:

    def on_get(self, req, resp):
        """
        Handles GET requests.

        Allows retrieving the warehouses of the respective user account.

        Args:
            req ([type]): The request object.
            resp ([type]): The response object.
        """
        warehouses = []

        for warehouse in self.db_conn.query(Warehouse).filter(UserWarehouse.user_id == self.user_id).join(UserWarehouse, UserWarehouse.warehouse_id == Warehouse.warehouse_id):
            warehouses.append({
                'id': warehouse.warehouse_id,
                'name': warehouse.name, 'description': warehouse.description, 
                'latitude': warehouse.latitude, 'longitude': warehouse.longitude
            })

        resp.media = {'warehouses': warehouses}
        resp.status = falcon.HTTP_200


    def on_post(self, req, resp):
        """
        Handles POST requests.

        Allows creating warehouse entities.

        Args:
            req ([type]): The request object.
            resp ([type]): The response object.
        """
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
            
            user_warehouse = UserWarehouse(warehouse_id=warehouse.warehouse_id,
                                           user_id=self.user_id, 
                                           permission='rw')

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

    def on_patch(self, req, resp, warehouse_id):
        """
        Handles PATCH requests.
        
        Allows editing warehouse entities fields.
        
        Args:
            req ([type]): The request object.
            resp ([type]): [description]The response object.
        """
        # Read warehouse details
        name = req.media.get('name')
        description = req.media.get('description')
        latitude = req.media.get('latitude')
        longitude = req.media.get('longitude')
        
        # If all details read are None
        if not any([name, description, latitude, longitude]):
            raise falcon.HTTPBadRequest('Bad Request', 'No warehouse parameters in request body.')

        # Get the warehouse from the user
        res = self.db_conn.query(Warehouse, UserWarehouse).join(UserWarehouse).filter(UserWarehouse.warehouse_id == warehouse_id).filter(UserWarehouse.user_id == self.user_id).first()

        # Check if the warehouse does not exist
        if res == None:
            raise falcon.HTTPNotFound(title='Not Found', description='Requested entity was not found.')

        warehouse = res[0]
        user_warehouse = res[1]

        # If user does not have write permission
        if 'w' not in user_warehouse.permission:
            raise falcon.HTTPForbidden('Forbidden', 'You do not have enough permissions for this action.')

        # Edit warehouse parameters
        if name != None:
            warehouse.name = name

        if description != None:
            warehouse.description = description

        if longitude != None:
            warehouse.longitude = longitude

        if latitude != None:
            warehouse.latitude = latitude

        # Add transaction
        self.db_conn.add(warehouse)

        # Commit modifications
        try:
            self.db_conn.commit()

        except Exception:

            # Rollback Changes
            self.db_conn.rollback()
            raise falcon.HTTPInternalServerError('Internal Server Error', 'An error ocurred, please inform the development team.')

        resp.media = {'success': 'Warehouse modified successfuly'}
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, warehouse_id):
        """
        Handles DELETE requests.
        
        Allows deleting warehouse entities.
        
        Args:
            req ([type]): The request object.
            resp ([type]): [description]The response object.
        """
        # Deletes warehouse from the current user account
        self.db_conn.query(UserWarehouse).filter_by(warehouse_id=warehouse_id, user_id=self.user_id).delete()

        # Commit modifications
        try:
            self.db_conn.commit()

        except Exception:

            # Rollback Changes
            self.db_conn.rollback()
            raise falcon.HTTPInternalServerError('Internal Server Error', 'An error ocurred, please inform the development team.')

        resp.media = {'success': 'Warehouse deleted successfuly'}
        resp.status = falcon.HTTP_200