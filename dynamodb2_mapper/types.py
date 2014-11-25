STRING = 'S'
NUMBER = 'N'
BINARY = 'B'
STRING_SET = 'SS'
NUMBER_SET = 'NS'
BINARY_SET = 'BS'
NULL = 'NULL'
BOOLEAN = 'BOOL'
MAP = 'M'
LIST = 'L'

QUERY_OPERATORS = {
    'eq': 'EQ',
    'lte': 'LE',
    'lt': 'LT',
    'gte': 'GE',
    'gt': 'GT',
    'beginswith': 'BEGINS_WITH',
    'between': 'BETWEEN',
}

FILTER_OPERATORS = {
    'eq': 'EQ',
    'ne': 'NE',
    'lte': 'LE',
    'lt': 'LT',
    'gte': 'GE',
    'gt': 'GT',
    # FIXME: Is this necessary? i.e. ``whatever__null=False``
    'nnull': 'NOT_NULL',
    'null': 'NULL',
    'contains': 'CONTAINS',
    'ncontains': 'NOT_CONTAINS',
    'beginswith': 'BEGINS_WITH',
    'in': 'IN',
    'between': 'BETWEEN',
}

JSON_TYPES = frozenset([list, dict])
