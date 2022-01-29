import logging
import traceback
from psycopg2 import connect, OperationalError

logger = logging.getLogger('db-init')

__connection_data = ""

try:
    connect(__connection_data).close()
except OperationalError:
    logger.error('Connection to database could not be established.')
    traceback.print_exc()
    exit(0)

logger.debug('Connections to database can be established.')

