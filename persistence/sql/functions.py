from typing import Any


class JoinTables:

    @staticmethod
    def join_tables(tables: list[tuple], table_context: Any, pk: str) -> str:
        tlb_union: str = ""
        tlb_join: str = ""

        for tbl in tables:
            tlb_union += f"{tbl[0]}.*, "
            tlb_join += f"JOIN {tbl[0]} ON {tbl[0]}.{tbl[1]}={table_context}.id "

        tlb_union += f"{table_context}.*"

        return """
            SELECT {} FROM {} {} WHERE {}.{}=%s;
        """.format(tlb_union, table_context, tlb_join, table_context, pk)
