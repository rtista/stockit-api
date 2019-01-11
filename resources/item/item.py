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
        if req.params['barcode']:
            
            res = self.db_conn.query(Item).filter_by(warehouse_id=warehouse_id, barcode=req.params['barcode'])

        else:
            res = self.db_conn.query(Item).filter_by(warehouse_id=warehouse_id)

        items = []

        # For each item in the warehouse
        for item in res:
            items.append({
                'id': item.item_id,
                'name': item.name, 'description': item.description, 
                'quantity': item.quantity, 'section': item.section,
                'barcode': item.barcode, 'user_id': item.user_id,
                'min_quantity': item.min_quantity
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
        description = req.media.get('description')
        quantity = req.media.get('quantity')
        barcode = req.media.get('barcode')
        section = req.media.get('section')
        min_quantity = req.media.get('min_quantity')

        # Check if parameters not empty
        if None in [name, description, quantity]:
            raise falcon.HTTPBadRequest('Bad Request', 'Missing name, description or quantity.')

        # Create item
        item = Item(name=name, description=description, quantity=quantity, 
                    section=section, barcode=barcode, warehouse_id=warehouse_id,
                    user_id=self.user_id, min_quantity=min_quantity)

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
        quantity = req.media.get('quantity')
        barcode = req.media.get('barcode')
        section = req.media.get('section')
        min_quantity = req.media.get('min_quantity')

        # If all details read are None
        if not any([name, description, quantity, barcode, section]):
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
            item.description = description

        if quantity != None:
            item.quantity = quantity

        if section != None:
            item.section = section

        if barcode != None:
            item.barcode = barcode

        if min_quantity != None:
            item.min_quantity = min_quantity

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