from __future__ import absolute_import

# Sorting stuffs
version_key = lambda name: int(name.split('_')[-1])

# Exception
class VersionError(Exception):
    """VersionError exception is raised when schema version could no be identied
    It may meam that the Python schema is *older* that the DB item or simply is
    not the right type.
    """

class Migration(object):
    """
    Migration engine base class. It defines all the magic to make things easy to
    use. To migrate a raw schema, only instanciate the migrator and "call" the
    instance with the raw_dict.

    >>> migrator = DataMigration()
    >>> migrated_raw_data = migrator(raw_data)

    Migrators must derive from this class and implement methods of the form
    - ``check_N(raw_data)`` -> returns True if raw_data is compatible with version N
    - ``migrate_to_N(raw_data)`` -> migrate from previous version to this one

    ``check_N`` are all called in the decreasing order. The first to return True
    determines the version.

    All migrators functions are called successively starting at N+1 assuming N
    is the current version number

    N version numbers do not need to be consecutive and are sorted in natural
    order.
    """
    _detectors = None
    _migrators = None

    def __init__(self, model):
        """
        Gather all the version detectors and migrators on the first call. They are
        then cached for all further instances.

        :param model: model class this migrator handles
        """
        cls = type(self)

        self.model = model

        # Did we already gather all this ?
        if cls._migrators is not None:
            return

        _detectors = []
        _migrators = []

        for key in dir(self):
            obj = getattr(self, key)
            if not callable(obj):
                continue
            if key.startswith("check_"):
                _detectors.append(key)
            if key.startswith("migrate_to_"):
                _migrators.append(key)

        cls._detectors = sorted(_detectors, key = version_key, reverse=True)
        cls._migrators = sorted(_migrators, key = version_key)

    def _detect_version(self, raw_data):
        """
        Detect the current schema version of this raw_data dict by calling ``check_N``
        in natural decreasing order. If the version checker returns ``True``, we
        consider this is the first compatible revision and return the number as
        ``current_revision``

        :param raw_data: Raw boto dict to migrate to latest version

        :return: current revision number

        :raises VersionError: when no check succeeded
        """
        for detector in type(self)._detectors:
            if getattr(self, detector)(raw_data):
                return version_key(detector)
        raise VersionError()

    def _do_migration(self, current_version, raw_data):
        """
        Run the migration engine engine. All ``migrate_to_N`` are called successively
        in natural ascending order as long as ``N > current_version``.

        :param current_version: Current version of the raw_data as detected by :py:meth:`~.Migration._detect_version`

        :param raw_data: Raw boto dict to migrate to latest version

        :return: Up to date raw boto dict
        """
        for migrator in type(self)._migrators:
            if version_key(migrator) > current_version:
                raw_data = getattr(self, migrator)(raw_data)
        return raw_data

    def __call__(self, raw_data):
        """
        Trigger the the 2 steps migration engine:

          1. detect the current version
          2. migrate to all newest versions

        :param raw_data: Raw boto dict to migrate to latest version

        :return: Up to date raw boto dict

        :raises VersionError: when no check succeeded
        """
        current_version = self._detect_version(raw_data)
        return self._do_migration(current_version, raw_data)
