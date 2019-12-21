# Third party imports
import falcon

class AuthResource:

    def on_get(self, req, resp):
        """Handle GET requests."""

        resp.media = {
            'methods': ['token']
        }

        resp.status = falcon.HTTP_200
