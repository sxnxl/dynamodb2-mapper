
class Attribute(object):
    __data_type__ = None
    __unique__ = False
    __nullable__ = True
    __default__ = None
    __value__ = None
    __hash_key__ = False
    __range_key__ = False
    __on_save__ = None
    __on_update__ = None

    def __init__(self):
        pass        

