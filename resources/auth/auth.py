# Third party imports
import falcon

class AuthResource:

    def on_get(self, req, resp):
        """Handle GET requests."""

        resp.media = {
            'methods': ['token']
        }

        resp.status_code = falcon.HTTP_200
