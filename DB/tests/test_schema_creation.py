import unittest

from sqlalchemy import inspect
from sqlalchemy_utils import drop_database

from DB.db import Base
from DB.db.managers.db_manager import DBManager
from DB.tests.test_utils import create_test_db_without_schemas


class CreateSchemaTest(unittest.TestCase):
    def setUp(self):
        self.config, self.engine = create_test_db_without_schemas()

        self.config.SHOULD_DROP_ALL_TABELS = False

    def test_create_schema(self):
        db_manager = DBManager(self.config)
        db_manager.load_schemas()
        ins = inspect(self.engine)
        # The clipping of the first table is because the first table is a meta table
        tables_from_db = sorted(ins.get_table_names()[1:])
        tables_to_be_inserted = sorted([t.name for t in Base.metadata.sorted_tables])
        self.assertEqual(tables_from_db, tables_to_be_inserted,
                         'the tables in the db don\'t match the tables that need to be created')

    def tearDown(self):
        drop_database(self.engine.url)
