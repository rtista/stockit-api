# Imports
from models import Warehouse, UserWarehouse, Item
from hooks import Authorize

# Batteries
from time import time

# Third party imports
import falcon
from sqlalchemy.exc import SQLAlchemyError, NoReferenceError

@falcon.before(Authorize())
class ItemResource:

    def on_get(self, req, resp, warehouse_id):
        """
        Handles GET requests.

        Allows retrieving the items of the given warehouse
        of the respective user account.

        Args:
            req ([type]): The request object.
            resp ([type]): The response object.
        """
        # Check user warehouse
        if self.db_conn.query(UserWarehouse).filter_by(user_id=self.user_id, warehouse_id=warehouse_id).first() == None:
            raise falcon.HTTPNotFound(title='Not Found', description='The requested warehouse does not exist.')

        # Query database
        # If request code exists add barcode to query
        if 'barcode' in req.params:
            
            res = self.db_conn.query(Item).filter_by(warehouse_id=warehouse_id, barcode=req.params['barcode'])

            # Return 404 if barcode is non-existent
            if res.count() == 0:
                raise falcon.HTTPNotFound(title='Not Found', description='The requested barcode does not exist.')

        else:
            res = self.db_conn.query(Item).filter_by(warehouse_id=warehouse_id)

        items = []

        # For each item in the warehouse
        for item in res:
            items.append({
                'id': item.item_id,
                'name': item.name, 'description': item.description.decode('utf-8'), 
                'barcode': item.barcode, 'available': item.available,
                'allocated': item.allocated, 'alert': item.alert,
                'user_id': item.user_id
            })

        resp.media = {'items': items}
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, warehouse_id):
        """
        Handles POST requests.

        Allows creating warehouse entities.

        Args:
            req ([type]): The request object.
            resp ([type]): The response object.
            warehouse_id (int): The warehouse id.
        """
        # Check user warehouse
        if self.db_conn.query(UserWarehouse).filter_by(user_id=self.user_id, warehouse_id=warehouse_id).first() == None:
            raise falcon.HTTPNotFound(title='Not Found', description='The requested warehouse does not exist.')

        # Read warehouse details
        name = req.media.get('name')
        description = req.media.get('description').encode('utf-8')
        barcode = req.media.get('barcode')
        available = req.media.get('available')
        allocated = req.media.get('allocated')
        alert = req.media.get('alert')

        # Check if parameters not empty
        if None in [name, description, available]:
            raise falcon.HTTPBadRequest('Bad Request', 'Missing name, description or quantity.')

        # Create item
        item = Item(name=name, description=description, barcode=barcode,
                    available=available, allocated=allocated, alert=alert,
                    warehouse_id=warehouse_id, user_id=self.user_id)

        self.db_conn.add(item)

        # Attempt database changes commit
        try:
            # Create item
            self.db_conn.commit()

        except SQLAlchemyError as e:

            # Rollback Changes
            self.db_conn.rollback()
            raise falcon.HTTPInternalServerError('Internal Server Error', 'Message: {}'.format(str(e)))

        resp.media = {'success': 'Item created successfuly'}
        resp.status = falcon.HTTP_201

    def on_patch(self, req, resp, warehouse_id, item_id):
        """
        Handles PATCH requests.
        
        Allows editing item entities fields.
        
        Args:
            req ([type]): The request object.
            resp ([type]): The response object.
            warehouse_id (int): The warehouse id.
            item_id (int): The item id.
        """
        # Check user warehouse
        if self.db_conn.query(UserWarehouse).filter_by(user_id=self.user_id, warehouse_id=warehouse_id).first() == None:
            raise falcon.HTTPNotFound(title='Not Found', description='The requested warehouse does not exist.')

        # Read warehouse details
        name = req.media.get('name')
        description = req.media.get('description')
        barcode = req.media.get('barcode')
        available = req.media.get('available')
        allocated = req.media.get('allocated')
        alert = req.media.get('alert')

        # If all details read are None
        if not any([name, description, barcode, available, allocated, alert]):
            raise falcon.HTTPBadRequest('Bad Request', 'No item parameters in request body.')

        # Get the item from the warehouse
        item = self.db_conn.query(Item).filter_by(item_id=item_id).first()

        # Check if the warehouse does not exist
        if item == None:
            raise falcon.HTTPNotFound(title='Not Found', description='Requested item does not exist.')

        # Edit warehouse parameters
        if name != None:
            item.name = name

        if description != None:
            item.description = description.encode('utf-8')

        if barcode != None:
            item.barcode = barcode

        if available != None:
            item.available = available

        if allocated != None:
            item.allocated = allocated

        if alert != None:
            item.alert = alert

        # Add transaction
        self.db_conn.add(item)

        # Commit modifications
        try:
            self.db_conn.commit()

        except Exception:

            # Rollback Changes
            self.db_conn.rollback()
            raise falcon.HTTPInternalServerError('Internal Server Error', 'An error ocurred, please inform the development team.')

        resp.media = {'success': 'Item modified successfuly'}
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, warehouse_id, item_id):
        """
        Handles DELETE requests.
        
        Allows deleting item entities.
        
        Args:
            req ([type]): The request object.
            resp ([type]): The response object.
            warehouse_id (int): The warehouse id.
            item_id (int): The item id.
        """
        # Check user warehouse
        if self.db_conn.query(UserWarehouse).filter_by(user_id=self.user_id, warehouse_id=warehouse_id).first() == None:
            raise falcon.HTTPNotFound(title='Not Found', description='The requested warehouse does not exist.')

        # Deletes warehouse from the current user account
        self.db_conn.query(Item).filter_by(item_id=item_id).delete()

        # Commit modifications
        try:
            self.db_conn.commit()

        except Exception:

            # Rollback Changes
            self.db_conn.rollback()
            raise falcon.HTTPInternalServerError('Internal Server Error', 'An error ocurred, please inform the development team.')

        resp.media = {'success': 'Item deleted successfuly'}
        resp.status = falcon.HTTP_200