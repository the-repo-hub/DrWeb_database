from unittest import TestCase

from main import Database


class DatabaseTests(TestCase):


    def setUp(self):
        super(DatabaseTests, self).setUp()
        self.database = Database()

    def test_simple_example(self):
        self.assertEqual(self.database.get("A"), self.database.NULL)
        self.database.set("A", '10')
        self.assertEqual(self.database.get("A"), '10')
        self.assertEqual(self.database.counts('10'), 1)
        self.database.set("B", '20')
        self.database.set("C", '10')
        self.assertEqual(self.database.counts('10'), 2)
        self.database.unset("B")
        self.assertEqual(self.database.get("B"), self.database.NULL)

    def test_transaction_example(self):
        self.database.begin()
        self.database.set("A", '10')
        self.database.begin()
        self.database.set("A", '20')
        self.database.begin()
        self.database.set("A", '30')
        self.assertEqual(self.database.get("A"), '30')
        self.database.rollback()
        self.assertEqual(self.database.get("A"), '20')
        self.database.commit()
        self.assertEqual(self.database.get("A"), '20')
        ###
        self.assertEqual(self.database._transaction_counter, 1)
        self.assertFalse(self.database._main_db.get(0))
        self.assertEqual(len(self.database._main_db.keys()), 2)

    def test_custom_transaction(self):
        self.database.set("A", '10') # 0
        self.database.begin() # 1
        self.database.set("A", '20')
        self.database.set("B", '20')
        self.database.set("C", '20')
        self.database.begin()# 2
        self.database.set("A", '10')
        self.database.begin()# 3
        self.assertEqual(self.database.find('10'), 'A')
        self.assertEqual(self.database.find('20'), 'B C')
        self.database.rollback()
        self.database.begin()# 3
        self.database.set("A", '30')
        self.database.commit() # 2
        self.assertEqual(self.database.find('10'), '')
        self.assertEqual(self.database.get("A"), '30')
        self.database.begin()
        self.database.begin()
        self.assertEqual(self.database.find('20'), 'B C')
        self.database.rollback()
        self.database.rollback()
        self.database.rollback()# 1
        self.assertEqual(self.database.get("A"), '20')
        self.assertEqual(self.database.get("B"), '20')

    def test_custom_commands(self):
        self.database.unset("A")
        self.database.set("A", '10')
        self.database.set("A", '10')
        self.database.set("B", '10')
        self.database.set("B", '10')
        self.database.set("C", '20')
        self.assertEqual(self.database.find('10'), "A B")
        self.assertEqual(self.database.find('20'), "C")
        self.assertEqual(self.database.counts('10'), 2)
        self.database.unset("B")
        self.assertEqual(self.database.find('10'), "A")
        self.assertEqual(self.database.get("B"), self.database.NULL)

    def test_second_custom_transaction(self):
        self.database.begin()
        self.database.unset("A")
        self.database.rollback()
        self.database.unset("A")
        self.assertEqual(self.database.get('A'), self.database.NULL)
        self.database.unset("A")
        self.database.unset('C')
        self.database.set("A", '10')
        self.database.set("B", '10')
        self.database.begin()
        self.database.set("C", '10')
        self.database.set("A", '20')
        self.database.begin()
        self.database.unset("C")
        self.database.set("B", '10')
        self.assertEqual(self.database.get("C"), self.database.NULL)
        self.assertEqual(self.database.get("D"), self.database.NULL)
        self.assertEqual(self.database.get("A"), '20')
        self.assertEqual(self.database.counts('10'), 1)
        self.assertEqual(self.database.counts("20"), 1)
        self.assertEqual(self.database.find('10'), 'B')
        self.assertEqual(self.database.counts("0"), 0)
        self.assertEqual(self.database.find('10'), 'B')
        self.assertEqual(self.database.find('20'), 'A')
        self.database.commit()
        self.database.rollback()
        self.assertEqual(self.database.get("A"), '10')
        self.assertEqual(self.database.get("B"), '10')
        self.database.begin()
        self.database.unset("C")
        self.database.unset("B")
        self.database.commit()
        self.database.commit()
        self.assertEqual(self.database.get("A"), '10')

    def test_example_second(self):
        self.database.set('A', '1')
        self.database.begin()
        self.database.set('A', '2')
        self.assertEqual(self.database.get('A'), '2')
        self.assertEqual(self.database.counts('2'), 1)
        self.assertEqual(self.database.counts('1'), 0)
        self.database.begin()
        self.database.unset('A')
        self.assertEqual(self.database.counts('2'), 0)
        self.assertEqual(self.database.counts('1'), 0)
        self.assertEqual(self.database.get('A'), self.database.NULL)
        self.database.commit()
        self.assertEqual(self.database.get('A'), '1')
        self.database.rollback()
        self.assertEqual(self.database.get('A'), '1')
