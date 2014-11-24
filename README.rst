DynamoDB2-mapper -- a DynamoDB object mapper, based on boto's dynamodb2 api.

Presentation
============

`DynamoDB <http://aws.amazon.com/dynamodb/>`_ is a minimalistic NoSQL engine
provided by Amazon as a part of their AWS product.

**DynamoDB** allows you to stores documents composed of unicode strings or numbers
as well as sets of unicode strings and numbers. Each tables must define a hash
key and may define a range key. All other fields are optional.

**DynamoDB2-mapper** brings a tiny abstraction layer over DynamoDB2 api to overcome
some of the limitations with no performance compromise. It is highly inspired by
the  `Dynamodb-mapper project <https://bitbucket.org/Ludia/dynamodb-mapper>`_

- **Report bugs**: https://github.com/sxnol/dynamodb2-mapper/issues 
- **Fork the code**: https://github.com/sxnol/dynamodb2-mapper
- **Download**: https://github.com/sxnol/dynamodb2-mapper/archive/master.zip

Requirements
============

 - Boto = https://github.com/kain-jy/boto/archive/develop.zip
 - AWS account

Highlights
==========

- Python <--> DynamoDB2 type mapping
- Default values


Example usage
=============

We assume you've correctly set your Boto credentials.

Quick install
-------------

::

    $ pip install https://github.com/sxnol/dynamodb2-mapper/archive/master.zip

If you have not yet configured Boto, you may simply

::

    $ export AWS_ACCESS_KEY_ID=<your id key here>
    $ export AWS_SECRET_ACCESS_KEY=<your secret key here>


First Model
-----------

::

    from random import random
    from dynamodb2_mapper.model import DynamoDB2Model
    from dynamodb2_mapper.types import STRING, NUMBER, DECIMAL
    from passlib.apps import custom_app_context as pwd_context

    class User(DynamoDB2Model):
        __tablename__ = 'users'
        username = Attribute(STRING, hash_key=True, unique=True)
        password = Attribute(STRING, nullable=False, on_save=pwd_context.encrypt, verify=lambda x,y: pwd_context.verify(y,x))
        rank = Attribute(DECIMAL, on_save=lambda x: x+0.1, default=random)
        register_timestamp = Attribute(TIMESTAMP, default=time(), indexed=True)


Initial Table creation
----------------------

::

    from dynamodb2_mapper.connection import DynamoDB2Connection

    conn = DynamoDB2Connection()
    conn.create_table(User, 10, 10, wait_for_active=True)


Model Usage
-----------

::

    import datetime
    from yourapp.models import User

    new_user = User()
    new_user.username = u"john_doe"
    new_user.password = u"secret"
    new_user.save()


    # Later on, retrieve that same object from the DB...
    existing_user = User(username=u"john_doe")
    existing_user = User(username__eq=u"john_doe")
    # or simply
    existing_user = User(u"john_doe")

    # rank will be increased by 0.1 and password will be hashed with new random salt
    existing_user.save() 

    # create custom methods which will take first argument as attribute's value
    existing_user.verify(u"secret")
    True

    existing_user.verify(u"baby")
    False

    # get users registered in last 10 days
    ten_days_ago = datetime.date.today() - datetime.timedelta(10)
    timestamp = ten_days_ago.strftime("%s")
    users_registered_in_last_ten_days = User().query(register_timestamp__gt=timestamp)

Contribute
==========

Want to contribute, report a but of request a feature ? The development goes on
at `sxnol's GitHub account <https://github.com/sxnol/dynamodb2-mapper>`_ :

DynamoDB2-mapper
---------------

- **Report bugs**: https://github.com/sxnol/dynamodb2-mapper/issues 
- **Fork the code**: https://github.com/sxnol/dynamodb2-mapper
- **Download**: https://github.com/sxnol/dynamodb2-mapper/archive/master.zip
