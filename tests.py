from unittest import TestCase

from main import Database


class DatabaseTests(TestCase):


    def setUp(self):
        super(DatabaseTests, self).setUp()
        self.database = Database()

    def test_simple_example(self):
        self.assertEqual(self.database.get("A"), self.database.NULL)
        self.database.set("A", 10)
        self.assertEqual(self.database.get("A"), 10)
        self.assertEqual(self.database.counts(10), 1)
        self.database.set("B", 20)
        self.database.set("C", 10)
        self.assertEqual(self.database.counts(10), 2)
        self.database.unset("B")
        self.assertEqual(self.database.get("B"), self.database.NULL)

    def test_transaction_example(self):
        self.database.begin()
        self.database.set("A", 10)
        self.database.begin()
        self.database.set("A", 20)
        self.database.begin()
        self.database.set("A", 30)
        self.assertEqual(self.database.get("A"), 30)
        self.database.rollback()
        self.assertEqual(self.database.get("A"), 20)
        self.database.commit()
        self.assertEqual(self.database.get("A"), 20)
        ###
        self.assertEqual(self.database._transaction_counter, 1)
        self.assertFalse(self.database._main_db.get(0))
        self.assertEqual(len(self.database._main_db.keys()), 2)

    def test_custom_transaction(self):
        self.database.set("A", 10) # 0
        self.database.begin() # 1
        self.database.set("A", 20)
        self.database.set("B", 20)
        self.database.set("C", 20)
        self.database.begin()# 2
        self.database.set("A", 10)
        self.database.begin()# 3
        self.database.rollback()
        self.database.begin()# 3
        self.database.set("A", 30)
        self.database.commit() # 2
        self.assertEqual(self.database.get("A"), 30)
        self.database.rollback()# 1
        self.assertEqual(self.database.get("A"), 20)
        self.assertEqual(self.database.get("B"), 20)

    def test_custom_commands(self):
        self.database.unset("A")
        self.database.set("A", 10)
        self.database.set("A", 10)
        self.database.set("B", 10)
        self.database.set("B", 10)
        self.database.set("C", 20)
        self.assertEqual(self.database.find(10), "A B")
        self.assertEqual(self.database.find(20), "C")
        self.assertEqual(self.database.counts(10), 2)
        self.database.unset("B")
        self.assertEqual(self.database.find(10), "A")
        self.assertEqual(self.database.get("B"), self.database.NULL)
