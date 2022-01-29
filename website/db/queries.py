from enum import Enum


class ClientQuery(Enum):
    pass


class AdminQuery(Enum):
    CREATE_SCHEMA = 0
    pass


queries = {}

with open('scripts/schema.sql') as f:
    queries[AdminQuery.CREATE_SCHEMA] = f.read()