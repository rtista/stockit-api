# Import required resources
from .auth import AuthResource, AuthTokenResource
# from .account import AccountResource
from .user import UserResource
from .warehouse import WarehouseResource
from .item import ItemResource


# The base point for each route
BASE_ENDPOINT ='/api'

# Declare all your routes here
ROUTES = {

    # Auth Module
    # TODO : Requires authentication token (System)
    '/auth': AuthResource,
    '/auth/token': AuthTokenResource,

    # User Module
    '/user': UserResource,

    # Warehouse Module
    '/warehouse': WarehouseResource,
    '/warehouse/{warehouse_id:int}': WarehouseResource,

    # Item Module
    '/warehouse/{warehouse_id:int}/item': ItemResource,
    '/warehouse/{warehouse_id:int}/item/{item_id:int}': ItemResource,
}
