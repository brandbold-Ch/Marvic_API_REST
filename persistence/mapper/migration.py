from psycopg2.errors import DuplicateTable
from utils.connection import DB
from tables import Tables


def migrate():
    try:
        for obj in Tables.migration_list():
            print(f"***** Migrating the table {obj[1]} *****")
            DB.execute(sentence=obj[0])

        print("### Migration finished ###")

    except DuplicateTable:
        print("+++ The tables already exist +++")


migrate()
