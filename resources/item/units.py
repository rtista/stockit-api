# Imports
from models import UserWarehouse, Item
from hooks import Authorize

# Third party imports
import falcon

@falcon.before(Authorize())
class UnitsResource:

    def on_post(self, req, resp, warehouse_id, item_id):
        """
        Handles POST requests.

        Allows incrementing item entities' units.

        Args:
            req ([type]): The request object.
            resp ([type]): The response object.
            warehouse_id (int): The warehouse id.
            item_id (int): The Item id.
        """
        # Check for valid unit query parameter
        if 'unit' not in req.params or req.params['unit'] not in ['available', 'allocated']:
            raise falcon.HTTPBadRequest(title='Bad Request', description='Please specify available or allocated units.')

        # Check user warehouse
        if self.db_conn.query(UserWarehouse).filter_by(user_id=self.user_id, warehouse_id=warehouse_id).first() == None:
            raise falcon.HTTPNotFound(title='Not Found', description='The requested warehouse does not exist.')

        # Get item from user warehouse
        item = self.db_conn.query(Item).filter_by(item_id=item_id).first()

        # If item does not exist
        if item == None:
            raise falcon.HTTPNotFound(title='Not Found', description='The requested item does not exist.')

        # Increment units value
        if req.params['unit'] == 'available':
            item.available += 1

        else:
            item.allocated += 1

        # Add transaction
        self.db_conn.add(item)

        # Commit modifications
        try:
            self.db_conn.commit()

        except Exception:

            # Rollback Changes
            self.db_conn.rollback()
            raise falcon.HTTPInternalServerError('Internal Server Error', 'An error ocurred, please inform the development team.')

        resp.media = {'Success': 'Increment successful'}
        resp.status = falcon.HTTP_200
