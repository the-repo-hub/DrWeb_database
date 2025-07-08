class Database:

    def __init__(self):
        self._transaction_counter = 0
        self._main_db = {self._transaction_counter: {}}
        self.db = self._main_db[self._transaction_counter]

    def get_val(self, key: str):
        print(self.db.get(key, 'NULL'))

    def set_val(self, key: str, val: int):
        self.db[key] = val

    def find(self, val: int):
        lst = [k for k, v in self.db.items() if v == val]
        print(" ".join(lst))

    def counts(self, val: int):
        print(list(self.db.values()).count(val))

    def unset(self, key):
        if self.db.get(key):
            self.db.pop(key)

    @staticmethod
    def end():
        exit(0)

    def begin(self):
        self._main_db[self._transaction_counter + 1] = self._main_db[self._transaction_counter].copy()
        self._transaction_counter += 1
        self.db = self._main_db[self._transaction_counter]

    def rollback(self):
        self._main_db.pop(self._transaction_counter)
        self._transaction_counter -= 1
        self.db = self._main_db[self._transaction_counter]

    def commit(self):
        self._main_db[self._transaction_counter - 1] = self._main_db[self._transaction_counter].copy()
        self._main_db.pop(self._transaction_counter)
        self._transaction_counter -= 1
        self.db = self._main_db[self._transaction_counter]

commands = {
    'GET': Database.get_val,
    'SET': Database.set_val,
    'FIND': Database.find,
    'COUNTS': Database.counts,
    'END': Database.end,
    'UNSET': Database.unset,
    'BEGIN': Database.begin,
    'ROLLBACK': Database.rollback,
    'COMMIT': Database.commit,
}

def main():
    database = Database()
    query = str()
    while query != "END":
        query = input()
        if not query:
            continue
        lst = query.split()
        command = lst.pop(0).upper()
        commands[command](database, *lst)

if __name__ == '__main__':
    main()