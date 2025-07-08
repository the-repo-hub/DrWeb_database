from typing import Union


class Database:
    NULL = 'NULL'

    def __init__(self):
        self._transaction_counter = 0
        self._main_db = {self._transaction_counter: {}}

    def get(self, key: str) -> Union[str, int]:
        c = self._transaction_counter
        while c >= 0:
            db = self._main_db[c]
            if key in db.keys():
                result = db.get(key)
                # if result is None (unset)
                return result if result else self.NULL
            c -= 1
        return self.NULL

    def set(self, key: str, val: str) -> None:
        db = self._main_db[self._transaction_counter]
        db[key] = val

    def find(self, val: str) -> str:
        c = self._transaction_counter
        variables = []
        while c >= 0:
            db = self._main_db[c]
            for k,v in db.items():
                if val == v and k not in variables:
                    # not set for ordering
                    variables.append(k)
            c -= 1
        return " ".join(variables)

    def counts(self, val: str) -> int:
        c = self._transaction_counter
        result = 0
        keys_set = set()
        while c >= 0:
            db = self._main_db[c]
            for key, value in db.items():
                if value == val and key not in keys_set:
                    result += 1
                    keys_set.add(key)
            c -= 1
        return result

    def unset(self, key: str) -> None:
        db = self._main_db[self._transaction_counter]
        if self._transaction_counter > 0:
            db[key] = None
        else:
            value = db.get(key)
            if value:
                del db[key]

    def end(self) -> None:
        exit(0)

    def begin(self) -> None:
        self._transaction_counter += 1
        self._main_db[self._transaction_counter] = {}

    def rollback(self) -> None:
        if self._transaction_counter > 0:
            del self._main_db[self._transaction_counter]
            self._transaction_counter -= 1

    def commit(self) -> None:
        if self._transaction_counter > 0:
            self._main_db[self._transaction_counter - 1].update(self._main_db[self._transaction_counter])
            del self._main_db[self._transaction_counter]
            self._transaction_counter -= 1
            db = self._main_db[self._transaction_counter]
            for key in set(db.keys()):
                if db.get(key) is None:
                    del self._main_db[self._transaction_counter][key]

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