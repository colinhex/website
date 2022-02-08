
import datetime
import logging
from typing import Callable, Any

from website.db import database

# ---------- Logging ----------
logger = logging.getLogger('Queries')

# ---------- Preferences ----------
__preferences: dict = {}


def set_pref(preferences):
    global __preferences
    __preferences = preferences

    database.set_pref(preferences)


# ---------- Queries ----------

# All supported queries for the server application.
queries = {
    'get_user_data_by_mail': None,
    'user_exists': None,
    'get_attribute_names': None,
    'get_user_data': None,
    'create_user': None,
    'create_post': None,
    'create_comment': None,
    'get_posts': None,
    'get_comments': None,
    'confirm_email': None
}


def load_query(query):
    with open('website/db/sql_scripts/{}.sql'.format(query)) as f:
        queries[query] = f.read()


def load_queries():
    for k, _ in queries.items():
        load_query(k)


load_queries()


# ---------- Utility ----------

def column_result_set_to_tuple(column_result_set: tuple):
    return tuple([tpl[0] for tpl in column_result_set])


def current_time():
    now = datetime.datetime.utcnow()
    return now.strftime("%Y/%m/%d %H:%M:%S")


# ---------- Sub-Queries -----------


def get_attribute_names(connection_data: dict, table: str) -> tuple:
    sub_connection_data = database.new_connection_data(connection_data['connection'], connection_data['key'])
    sub_connection_data['query'] = queries['get_attribute_names']
    sub_connection_data['args'] = [table]
    return column_result_set_to_tuple(database.execute(sub_connection_data))


def get_user_data(connection_data: dict, user_id: str) -> dict:
    sub_connection_data = database.new_connection_data(connection_data['connection'], connection_data['key'])
    sub_connection_data['query'] = queries['get_user_data']
    sub_connection_data['args'] = [user_id]
    result_set_user_data = database.execute(sub_connection_data)[0]  # Only one result
    result_set_attr_names = get_attribute_names(sub_connection_data, 'users')
    return dict(zip(result_set_attr_names, result_set_user_data))


# ---------- Server Interface ----------


def get_posts(user_id: str) -> Any:
    connection_data = database.get_connection(user_id)
    connection_data['query'] = queries['get_posts']
    attribute_names = get_attribute_names(connection_data, 'posts')
    posts = database.execute(connection_data, True)
    return [dict(zip(attribute_names, post)) for post in posts]


def get_comments(user_id: str) -> Any:
    connection_data = database.get_connection(user_id)
    connection_data['query'] = queries['get_comments']
    attribute_names = get_attribute_names(connection_data, 'comments')
    comments = database.execute(connection_data, True)
    return [dict(zip(attribute_names, comment)) for comment in comments]


def create_user(user_id: str, email: str, password: str,
                hash_: Callable[[str], str], encrypt_: Callable[[str], str]) -> None:
    connection_data = database.get_connection(user_id)
    connection_data['query'] = queries['create_user']
    connection_data['args'] = [user_id, encrypt_(email), hash_(password), current_time()]
    database.execute(connection_data, True)


def create_post(user_id: str, title: str, text: str, href=None) -> None:
    connection_data = database.get_connection(user_id)
    connection_data['query'] = queries['create_post']
    connection_data['args'] = [user_id, current_time(), text, href, title]
    database.execute(connection_data, True)


def create_comment(user_id: str, text: str, parent_id: str) -> None:
    connection_data = database.get_connection(user_id)
    connection_data['query'] = queries['create_comment']
    connection_data['args'] = [user_id, current_time(), text, parent_id]
    database.execute(connection_data, True)


def verify_password(user_id: str, password: str, verify: Callable[[str, str], bool]) -> bool:
    connection_data = database.get_connection(user_id)
    user_data = get_user_data(connection_data, user_id)
    database.abandon_connection(connection_data)
    return verify(password, user_data['password'])


def confirm_email(user_id) -> None:
    connection_data = database.get_connection(user_id)
    connection_data['query'] = queries['confirm_email']
    connection_data['args'] = [user_id]
    database.execute(connection_data, True)


def user_exists(user_id) -> bool:
    connection_data = database.get_connection(user_id)
    connection_data['query'] = queries['user_exists']
    return len(database.execute(connection_data, True)) != 0


def get_user(user_id) -> dict:
    connection_data = database.get_connection(user_id)
    user_data = get_user_data(connection_data, user_id)
    database.abandon_connection(connection_data)
    return user_data


def get_user_by_mail(user_id, email, encrypt) -> dict:
    connection_data = database.get_connection(user_id)
    connection_data['query'] = queries['get_user_data_by_mail']
    connection_data['args'] = [encrypt(email)]
    return database.execute(connection_data, True)[0]
