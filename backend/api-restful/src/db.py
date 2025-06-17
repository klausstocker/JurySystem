from colorama import Fore
import datetime
import base64
import aiomysql
import asyncio


class DatabaseConnections:
    def __init__(self, username=None, password=None, host=None, port=None, database=None):
        self.pool = None
        self.database = database
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    def decode_token(self, base64_bytes) -> tuple[str, str]:
        """
        Decodes a base64-encoded token and extracts the username and password.

        The function takes a base64-encoded string representing a concatenation
        of a username and password, separated by a colon (:). It decodes the
        token, splits it into the username and password, and returns them as
        separate strings.
        """
        token_bytes = base64.b64decode(base64_bytes)
        untoken = token_bytes.decode('ascii')
        base64_user, base64_pass = untoken.split(":", 1)
        return base64_user, base64_pass

    async def fetch(self, sql: str = str(), all: bool = False):
        """
        Fetch data from the database with the provided SQL query and fetch mode. This
        function executes the given SQL query and retrieves the result(s) based on the
        specified fetching mode.

        This is an asynchronous function utilizing a connection pool to acquire a
        connection to the database and execute the SQL query efficiently. It supports
        two fetching modes: fetching a single result or fetching all results.
        """
        print(f'SQL: {sql}')
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                result = await cursor.fetchall() if all else await cursor.fetchone()
                return result

    async def sql_exec(self, sql, values):
        """
        Executes an SQL command asynchronously and commits the transaction. This function is
        intended for use with a connection pool. It provides a way to run SQL commands while
        automatically managing connections and cursors.
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, values)
                await conn.commit()
                return cursor.lastrowid

    async def sql_commit(self, sql):
        """
        Executes the given SQL query and commits the transaction to the database. This function
        uses asynchronous database connection management to ensure efficiency and ensure that
        resources are appropriately cleaned up after the operation.
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                await conn.commit()
                return cursor.rowcount

    async def sql_insert(self, sql, values):
        """
        Executes an SQL INSERT statement asynchronously with provided SQL syntax and
        arguments, commits the transaction, and returns the last inserted row ID.
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, values)
                await conn.commit()
                return cursor.lastrowid

    async def connect(self):
        timestamp = lambda: datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        print(f'{Fore.GREEN}{timestamp()}[DB] Create connection pool for {self.host}:{self.port}')
        print(f'user={self.username}, password={self.password}')
        try:
            self.pool = await aiomysql.create_pool(host=self.host, port=int(self.port),
                                                   user=self.username, password=self.password,
                                                   db=self.database, loop=asyncio.get_event_loop())
            print(f'{Fore.GREEN}{timestamp()}[DB] Connected to {self.host}:{self.port}')
        except Exception as e:
            print(f'{Fore.RED}{timestamp()}[DB] Could not connect to database and create the connection pool: {e}')
            await asyncio.sleep(5)
            raise e

    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()
