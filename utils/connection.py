from psycopg2.extensions import connection, cursor
from psycopg2.sql import Composed
from dotenv import load_dotenv
import psycopg2
import os


class DB:

    def connection_db() -> connection:
        load_dotenv()

        url: str = os.getenv("URL_DATABASE")
        config: dict = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("USER"),
            "password": os.getenv("PASSWORD"),
            "host": os.getenv("HOST"),
            "port": os.getenv("PORT")
        }

        return psycopg2.connect(url)

    @classmethod
    def execute(cls, sentence: str | Composed, give: bool = False, parameters=None) -> None | list:
        data = None

        con: connection = cls.connection_db()
        executor: cursor = con.cursor()
        executor.execute(query=sentence, vars=parameters)

        if give:
            data = executor.fetchall()

        con.commit()
        executor.close()
        con.close()

        return data
