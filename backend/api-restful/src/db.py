from fastapi import FastAPI, HTTPException, status, requests
from colorama import Fore
import datetime
import base64
import aiomysql
import asyncio
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from mediatypes import MediaTypes

media_types = MediaTypes()


class DatabaseConnections:
    pool = None


async def post_sql(sql_query=None, ):
    """
    Executes a given SQL query asynchronously and returns the results in JSON format. The function supports queries
    that either return rows or that involve updates/commands without rows.
    Returns JSONResponse containing the results of the SQL query. The HTTP status code in the response represents
    the outcome of the query:
    - 200 (OK): If the query returns rows.
    - 201 (Created): If the query executes successfully without returning rows.
    - 202 (Accepted): If no SQL query is provided or execution yields no specific results.
    """
    async with connections.pool.acquire() as connection:
        async with connection.cursor() as cursor:
            try:
                results = await cursor.execute(sql_query)
                for result in results:
                    if result.with_rows:
                        return JSONResponse(result, status_code=status.HTTP_200_OK,
                                            media_type=media_types.APPLICATION_JSON)
                    await connection.commit()
                    return JSONResponse(result, status_code=status.HTTP_201_CREATED,
                                        media_type=media_types.APPLICATION_JSON)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}")

        return JSONResponse(content={}, status_code=status.HTTP_202_ACCEPTED)


def decode_token(base64_bytes) -> tuple[str, str]:
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


async def fetch(sql: str = str(), all: bool = False):
    """
    Fetch data from the database with the provided SQL query and fetch mode. This
    function executes the given SQL query and retrieves the result(s) based on the
    specified fetching mode.

    This is an asynchronous function utilizing a connection pool to acquire a
    connection to the database and execute the SQL query efficiently. It supports
    two fetching modes: fetching a single result or fetching all results.
    """
    print(f'SQL: {sql}')
    async with connections.pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(sql)
            result = await cursor.fetchall() if all else await cursor.fetchone()
            return result


async def sql_exec(sql, values):
    """
    Executes an SQL command asynchronously and commits the transaction. This function is
    intended for use with a connection pool. It provides a way to run SQL commands while
    automatically managing connections and cursors.
    """
    async with connections.pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(sql, values)
            await connection.commit()
            return cursor.lastrowid


async def sql_commit(sql):
    """
    Executes the given SQL query and commits the transaction to the database. This function
    uses asynchronous database connection management to ensure efficiency and ensure that
    resources are appropriately cleaned up after the operation.
    """
    async with connections.pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(sql)
            await connection.commit()
            return cursor.rowcount


async def sql_insert(sql, values):
    """
    Executes an SQL INSERT statement asynchronously with provided SQL syntax and
    arguments, commits the transaction, and returns the last inserted row ID.
    """
    async with connections.pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(sql, values)
            await connection.commit()
            return cursor.lastrowid


async def connect():
    host = 'localhost'
    port = 3311
    user = 'foo'
    base = 'foo'
    password = 'foo'
    timestamp = lambda: datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    print(f'{Fore.GREEN}{timestamp()}[DB] Create connection pool for {host}:{port}')
    print(f'user={user}, password={password}')
    try:
        connections.pool = await aiomysql.create_pool(host=host, port=int(port),
                                                      user=user, password=password,
                                                      db=base, loop=asyncio.get_event_loop())
        print(f'{Fore.GREEN}{timestamp()}[DB] Connected to {host}:{port}')
    except Exception as e:
        print(f'{Fore.RED}{timestamp()}[DB] Could not connect to database and create the connection pool: {e}')
        await asyncio.sleep(5)
        raise e


async def close():
    connections.pool.close()
    await connections.pool.wait_closed()


connections = DatabaseConnections()
