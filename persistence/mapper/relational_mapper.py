from persistence.sql.manipulation_language import DML
from persistence.sql.functions import JoinTables
from utils.connection import DB
from typing import Any


class RelationalMapper:

    def __init__(self, _obj: Any) -> None:
        self.name_class: str = _obj.__class__.__name__
        self._obj = _obj

    def set(self, **kwargs) -> None:
        parsed: list = [f"'{x}'" for x in kwargs.values()]
        DB.execute(
            sentence=DML.insert(self.name_class, ', '.join(list(kwargs.keys())), ', '.join(parsed)),
            parameters=None
        )

    def get(self, join_tables: list[tuple] = None, **kwargs) -> None:
        key, value = list(kwargs.items())[0]

        records: list = DB.execute(
            sentence=DML.select(self.name_class, key),
            parameters=[value],
            give=True
        )

        if records:
            if join_tables:
                print(DB.execute(
                    sentence=JoinTables.join_tables(join_tables, self.name_class, key),
                    parameters=[value],
                    give=True
                ))
            self.compose_attributes(records)

    def delete(self, **kwargs): ...

    def update(self, **kwargs): ...

    def compose_attributes(self, values) -> None:
        attr_all = self._obj.__dict__
        for count, attr in enumerate(list(attr_all.items())[2:]):
            self._obj.__setattr__(attr[0], values[0][count])
