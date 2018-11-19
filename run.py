#!/usr/bin/env python3

# Own Imports
from resources import BASE_ENDPOINT, ROUTES
from middleware import MySQLSessionManager
from config import AppConfig
from models import Base

# Third party imports
import falcon
import bjoern

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

##################################
# MySQL Connection Configuration #
##################################
engine = create_engine(
    '{engine}://{username}:{password}@{host}:{port}/{dbname}'.format(**AppConfig.MYSQL)
)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

####################################
# MySQL Table Models Configuration #
####################################
try:
    Base.metadata.create_all(engine)

except OperationalError as e:
    print('Operational Error\nCode: {}\nMessage: {}'.format(e.orig.args[0], e.orig.args[1]))
    exit(1)

############################
# Falcon API Configuration #
############################

# Middleware Configuration
api = falcon.API(
        middleware=[
            MySQLSessionManager(Session)
        ]
    )

#################
# Route Loading #
#################
for route in ROUTES:
    api.add_route('{}{}'.format(BASE_ENDPOINT, route), ROUTES[route]())


# Serve application
if __name__ == '__main__':

    print('Starting bjoern server on {}:{}'.format(AppConfig.SERVER['url'], AppConfig.SERVER['port']))
    bjoern.listen(api, AppConfig.SERVER['url'], AppConfig.SERVER['port'])
    bjoern.run()
