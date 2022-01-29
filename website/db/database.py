
from psycopg2.pool import ThreadedConnectionPool

__connection_data = ""

__connection_pool = ThreadedConnectionPool(0, 5, __connection_data)


def get_connection(key: str):
    return __connection_pool.getconn(key)


def abandon_connection(conn, key: str):
    __connection_pool.putconn(conn, key, close=False)

