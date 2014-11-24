from __future__ import absolute_import

import unittest

from dynamodb_mapper.model import DynamoDBModel
from dynamodb_mapper.migration import Migration, VersionError

# test case: field rename rename
class UserMigration(Migration):
    def check_1(self, raw_data):
        field_count = 0
        field_count += u"id" in raw_data and isinstance(raw_data[u"id"], unicode)
        field_count += u"energy" in raw_data and isinstance(raw_data[u"energy"], int)
        field_count += u"mail" in raw_data and isinstance(raw_data[u"mail"], unicode)

        return field_count == len(raw_data)

    #No migrator for version 1, of course !

    def check_2(self, raw_data):
        # Stub. This is to check checker sorting only
        return False

    def migrate_to_2(self, raw_data):
        # Stub. This is to check migrator sorting only
        return raw_data

    def check_11(self, raw_data):
        field_count = 0
        field_count += u"id" in raw_data and isinstance(raw_data[u"id"], unicode)
        field_count += u"energy" in raw_data and isinstance(raw_data[u"energy"], int)
        field_count += u"email" in raw_data and isinstance(raw_data[u"email"], unicode)

        return field_count == len(raw_data)

    def migrate_to_11(self, raw_data):
        raw_data[u"email"] = raw_data[u"mail"]
        del raw_data[u"mail"]
        return raw_data

class User(DynamoDBModel):
    __table__ = "user"
    __hash_key__ = "id"
    __migrator__ = UserMigration
    __schema__ = {
        "id": unicode,
        "energy": int,
        "email": unicode
    }

class TestMigration(unittest.TestCase):
    def test_init(self):
        # check migrator list + natural order sort
        m = UserMigration(User)
        self.assertEquals(m._detectors, ['check_11', 'check_2', 'check_1'])
        self.assertEquals(m._migrators, ['migrate_to_2', 'migrate_to_11'])

    def test_version_detection_error(self):#TODO test exception
        raw_data_version_error_type = {
            u"id": u"Jackson",
            u"energy": 6742348,
            u"mail": "jackson@tldr-ludia.com",
        }

        raw_data_version_error_field = {
            u"id": u"Jackson",
            u"energy": 6742348,
            u"e-mail": u"jackson@tldr-ludia.com",
        }

        m = UserMigration(User)
        self.assertRaises(
            VersionError,
            m._detect_version,
            raw_data_version_error_type,
        )

    def test_version_detection(self):#TODO test exception
        raw_data_version_1_regular = {
            u"id": u"Jackson",
            u"energy": 6742348,
            u"mail": u"jackson@tldr-ludia.com",
        }

        # Version 1 with no mail is detected as 11 as the migration is on mail field
        raw_data_version_1_no_mail = {
            u"id": u"Jackson",
            u"energy": 6742348,
        }

        m = UserMigration(User)
        self.assertEquals(m._detect_version(raw_data_version_1_regular), 1)
        self.assertEquals(m._detect_version(raw_data_version_1_no_mail), 11)

    def test_migration(self):
        raw_data_version_1 = {
            u"id": u"Jackson",
            u"energy": 6742348,
            u"mail": u"jackson@tldr-ludia.com",
        }

        raw_data_version_11 = {
            u"id": u"Jackson",
            u"energy": 6742348,
            u"email": u"jackson@tldr-ludia.com",
        }

        m = UserMigration(User)
        self.assertEquals(m._do_migration(1, raw_data_version_1), raw_data_version_11)
        self.assertEquals(m._detect_version(raw_data_version_11), 11)

    def test_auto_migration(self):
        raw_data_version_1 = {
            u"id": u"Jackson",
            u"energy": 6742348,
            u"mail": u"jackson@tldr-ludia.com",
        }

        raw_data_version_11 = {
            u"id": u"Jackson",
            u"energy": 6742348,
            u"email": u"jackson@tldr-ludia.com",
        }

        m = UserMigration(User)
        self.assertEquals(m(raw_data_version_1), raw_data_version_11)

    # more a functional test than a unit test...
    def test_real_model_migration(self):
        raw_data_version_1 = {
            u"id": u"Jackson",
            u"energy": 6742348,
            u"mail": u"jackson@tldr-ludia.com",
        }

        raw_data_version_11 = {
            u"id": u"Jackson",
            u"energy": 6742348,
            u"email": u"jackson@tldr-ludia.com",
        }

        user = User._from_db_dict(raw_data_version_1)
        # Raw_data still original => needed for ROC
        self.assertEquals(user._raw_data, raw_data_version_1)
        # Data is at latest revision => consistency
        self.assertEquals(user._to_db_dict(), raw_data_version_11)
        # check the migrator engine is persisted (cache)
        assert isinstance(User.__migrator__, UserMigration)
