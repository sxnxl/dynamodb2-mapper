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

- Python <--> DynamoDB type mapping
- Deep schema definition and validation with ``Onctuous`` (new in 1.8.0)
- Multi-target transaction (new in 1.6.0)
- Sub-transactions (new in 1.6.2)
- Migration engine (new in 1.7.0)
- Smart conflict detection (new in 1.7.0)
- Full low-level chunking abstraction for ``scan``, ``query`` and ``get_batch``
- Default values
- Auto-inc hash_key
- Framework agnostic


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

    from dynamodb2_mapper.model import Dynamo2DBModel
    from dynamodb2_mapper.types import STRING, NUMBER

    class User(DynamoDB2Model):
        __tablename__ = 'users'
        username = Attribute(STRING, hash_key=True, unique=True)
        password = Attribute(STRING, nullable=False, on_save=)


    class DoomMap(DynamoDBModel):
        __table__ = u"doom_map"
        __hash_key__ = u"episode"
        __range_key__ = u"map"
        __schema__ = {
            u"episode": int,
            u"map": int,
            u"name": unicode,
            u"cheats": set,
        }
        __defaults__ = {
            "cheats": set([u"Konami"]),
        }


Initial Table creation
----------------------

::

    from dynamodb_mapper.model import ConnectionBorg

    conn = ConnectionBorg()
    conn.create_table(DoomMap, 10, 10, wait_for_active=True)


Model Usage
-----------

::

    e1m1 = DoomMap()
    e1m1.episode = 1
    e1m1.map = 1
    e1m1.name = u"Hangar"
    e1m1.cheats = set([u"idkfa", u"iddqd", u"idclip"])
    e1m1.save()


    # Later on, retrieve that same object from the DB...
    e1m1 = DoomMap.get(1, 1)

    # query all maps of episode 1
    e1_maps = DoomMap.query(hash_key=1)

    # query all maps of episode 1 with 'map' hash_key > 5
    from boto.dynamodb.condition import GT
    e1_maps_after_5 = DoomMap.query(
        hash_key=1,
        range_key_condition=GT(5))

Contribute
==========

Want to contribute, report a but of request a feature ? The development goes on
at `sxnol's GitHub account <https://github.com/sxnol/dynamodb2-mapper>`_ :

DynamoDB2-mapper
---------------

- **Report bugs**: https://github.com/sxnol/dynamodb2-mapper/issues 
- **Fork the code**: https://github.com/sxnol/dynamodb2-mapper
- **Download**: https://github.com/sxnol/dynamodb2-mapper/archive/master.zip
