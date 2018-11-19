# Import required resources
from .auth import AuthResource, AuthTokenResource
from .account import AccountResource


# The base point for each route
BASE_ENDPOINT ='/api'

# Declare all your routes here
ROUTES = {

    # Auth Module
    '/auth': AuthResource,
    '/auth/token': AuthTokenResource,

    # Account Module
    '/account': AccountResource,
}
