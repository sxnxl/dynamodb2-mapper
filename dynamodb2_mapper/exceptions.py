class SchemaError(Exception):
    """SchemaError exception is raised when a schema consistency check fails.
    Most of the checks are performed in :py:meth:`~.ConnectionBorg.create_table`.

    Common consistency failure includes lacks of ``__table__``, ``__hash_key__``,
    ``__schema__`` definition or when an :py:class:`~.autoincrement_int` ``hash_key``
    is used with a ``range_key``.
    """


class MaxRetriesExceededError(Exception):
    """Raised when a failed operation couldn't be completed after retrying
    ``MAX_RETRIES`` times (e.g. saving an autoincrementing hash_key).
    """


class ConflictError(Exception):
    """Atomic edition failure.
    Raised when an Item has been changed between the read and the write operation
    and this has been forbid by the ``raise_on_conflict`` argument of
    :meth:`DynamoDBModel.save` (i.e. when somebody changed the DB's version of
    your object behind your back).
    """


class OverwriteError(ConflictError):
    """Raised when saving a DynamoDBModel instance would overwrite something
    in the database and we've forbidden that because we believe we're creating
    a new one (see :meth:`DynamoDBModel.save`).
    """


class InvalidRegionError(Exception):
    """Raised when ``set_region()`` is called with an invalid region name.
    """



