import datetime
from decimal import Decimal

def current_timestamp():
    return Decimal(datetime.datetime.now().strftime('%s.%f'))
