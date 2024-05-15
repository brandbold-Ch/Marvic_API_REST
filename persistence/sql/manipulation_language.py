

class DML:

    @staticmethod
    def insert(table: str, fields: str, values: str) -> str:
        return ("INSERT INTO {} ({}) VALUES ({})"
                .format(table, fields, values))

    @staticmethod
    def select(table: str, selector: str) -> str:
        return "SELECT * FROM {} WHERE {}=%s".format(table, selector)
