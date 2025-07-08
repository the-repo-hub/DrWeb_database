from typing import Union

class Database:
    NULL = 'NULL'

    def __init__(self):
        self._transaction_counter = 0
        self._main_db = {self._transaction_counter: {}}
        self.db = self._main_db[self._transaction_counter]

    def get(self, key: str) -> Union[str, int]:
        return self.db.get(key, self.NULL)

    def set(self, key: str, val: int) -> None:
        self.db[key] = val

    def find(self, val: int) -> str:
        lst = [k for k, v in self.db.items() if v == val]
        return " ".join(lst)

    def counts(self, val: int) -> int:
        return list(self.db.values()).count(val)

    def unset(self, key: str) -> None:
        if self.db.get(key):
            self.db.pop(key)

    def end(self) -> None:
        exit(0)

    def begin(self) -> None:
        self._main_db[self._transaction_counter + 1] = self._main_db[self._transaction_counter].copy()
        self._transaction_counter += 1
        self.db = self._main_db[self._transaction_counter]

    def rollback(self) -> None:
        if self._transaction_counter > 0:
            self._main_db.pop(self._transaction_counter)
            self._transaction_counter -= 1
            self.db = self._main_db[self._transaction_counter]

    def commit(self) -> None:
        if self._transaction_counter > 0:
            self._main_db[self._transaction_counter - 1] = self._main_db[self._transaction_counter].copy()
            self._main_db.pop(self._transaction_counter)
            self._transaction_counter -= 1
            self.db = self._main_db[self._transaction_counter]

commands = {
    'GET': Database.get,
    'SET': Database.set,
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
    try:
        while query != "END":
            query = input()
            if not query:
                continue
            lst = query.split()
            command = lst.pop(0).upper()
            result = commands[command](database, *lst)
            if result:
                print(result)
    except EOFError:
        database.end()
    except KeyboardInterrupt:
        database.end()

if __name__ == '__main__':
    main()