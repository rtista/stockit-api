class MySQLSessionManager:
    """
    Create a scoped session for every request and
    closes it when the request ends.
    """

    def __init__(self, SessionManager):
        self.Session = SessionManager

    def process_resource(self, req, resp, resource, params):
        resource.db_conn = self.Session()

    def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(resource, 'db_conn'):
            if not req_succeeded:
                resource.db_conn.rollback()
            self.Session.remove()
