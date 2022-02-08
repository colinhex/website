from typing import Any
import logging
from psycopg2.pool import ThreadedConnectionPool

# ---------- Database Connection Logging ----------
logger = logging.getLogger('Database')

# ---------- Database Connection ----------
__connection_pool: ThreadedConnectionPool = Any

# ---------- Preferences ----------
__preferences: dict = {}


def set_pref(preferences):
    global __preferences
    __preferences = preferences

    global __connection_pool
    __connection_pool = ThreadedConnectionPool(0, 5, __preferences['conn'], options='-c search_path=general')


#  ---------- Database Connection Utility ----------


def new_connection_data(connection, key) -> dict:
    return {
        'connection': connection,
        'key': key,
        'query': None,
        'args': None
    }


def get_connection(key: str) -> dict:
    logger.debug('Handing out connection for key: ' + key)
    connection = __connection_pool.getconn(key)
    connection.autocommit = True
    return new_connection_data(connection, key)


def abandon_connection(connection_data: dict) -> None:
    logger.debug('Abandoning connection with key: ' + connection_data['key'])
    __connection_pool.putconn(connection_data['connection'], connection_data['key'], close=False)


def execute(connection_data: dict, abandon=False) -> Any:
    if not connection_data['query']:
        raise ValueError('No query given to execute')

    logger.debug('Executing query on connection with key: ' + connection_data['key'] +
                 '\nQuery:\n{}\n{}'.format('-' * 20, connection_data['query']) +
                 '\n<-- Args: {}\n{}'.format(connection_data['args'], '-' * 20))

    with connection_data['connection'].cursor() as curs:
        if connection_data['args']:
            curs.execute(connection_data['query'], connection_data['args'])
        else:
            curs.execute(connection_data['query'])
        result = curs.fetchall() if curs.description else None
        if abandon:
            abandon_connection(connection_data)
        logger.debug('Query from connection with key: ' + connection_data['key'] +
                     ' returned result: ' + str(result))
        return result
