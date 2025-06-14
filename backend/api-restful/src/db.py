from fastapi import FastAPI, HTTPException, status, requests
from colorama import Fore
import datetime
import base64
import aiomysql
import asyncio
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from http_status_codes import HTTP_NOT_FOUND, HTTP_BAD_REQUEST, HTTP_CREATED


class Connections:
    pool = None


def post_sql():
    """post: sql."""
    post = request.data
    sql = post.decode('utf-8')

    cnx = sql_connection()
    cur = cnx.cursor(buffered=True)

    try:
        for result in cur.execute(sql, multi=True):

            if result.with_rows:
                return jsonify(result.fetchall()), 200

            cnx.commit()
            return jsonify(status=201,
                           statment=result.statement,
                           rowcount=result.rowcount,
                           lastrowid=result.lastrowid), 201
    finally:
        cur.close()
        cnx.close()

    return jsonify(status=202, method='POST'), 202


async def post_json(database, table, json_data=None) -> JSONResponse:
    """post: json data application/json."""
    post = json_data

    # fields = ",".join([str(key) for key in post])
    # placeholders = ['%s'] * len(post)
    # places = ",".join([str(key) for key in placeholders])
    places = ",".join(['%s'] * len(post))
    fields = ",".join(post)

    records = [value for value in post.values()]

    sql = f"INSERT INTO {database}.{table} ({fields}) VALUES ({places})"
    insert = await sqlexec(sql, records)

    reply = {'status': HTTP_CREATED, 'message': "Created", 'insert': True, 'rowid': insert} if insert > 0 \
        else {'status': HTTP_BAD_REQUEST, 'message': "Failed Create", 'insert': False}

    return JSONResponse(jsonable_encoder(reply), status_code=reply.get('status'), media_type="application/json")


async def post_form(database, table):
    """post: form data application/x-www-form-urlencoded."""
    credentials = request.form.get('credentials', None)

    if credentials:

        columns = []
        records = []
        for key in request.form.keys():
            if key == 'credentials':
                continue
            columns.append(key)
            records.append(request.form[key])

        count = len(request.form) - 1
        placeholders = ['%s'] * count

        places = ",".join([str(key) for key in placeholders])

        fields = ",".join([str(key) for key in columns])

        base64_user, base64_pass = base64_untoken(credentials.encode('ascii'))

        sql = "INSERT INTO " + database + "." + table
        sql += " (" + fields + ") VALUES (" + places + ")"

        insert = sqlinsert(sql, records, base64_user, base64_pass)

        if insert > 0:
            return jsonify(status=201,
                           message="Created",
                           method="POST",
                           insert=True,
                           rowid=insert), 201

        return jsonify(status=461,
                       message="Failed Create",
                       method="POST",
                       insert=False), 461

    return jsonify(status=401,
                   message='Unauthorized',
                   details='No valid authentication credentials for target resource',
                   method='POST',
                   insert=False), 401


def base64_untoken(base64_bytes):
    """base64: untoken."""
    token_bytes = base64.b64decode(base64_bytes)
    untoken = token_bytes.decode('ascii')
    base64_user = untoken.split(":", 1)[0]
    base64_pass = untoken.split(":", 1)[1]
    return base64_user, base64_pass


async def fetchall(sql):
    """sql: fetchall."""
    async with connections.pool.acquire() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(sql)
            rows = await cur.fetchall()
            await cur.close()
            cnx.close()
    return rows


async def fetch(sql: str = str(), all: bool = False):
    """Fetch a single row from the database."""
    print(f'SQL: {sql}')
    async with connections.pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(sql)
            result = await cursor.fetchall() if all else await cursor.fetchone()
            return result


async def fetchone_alt(sql):
    """sql: fetchone."""
    async with connections.pool.acquire() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(sql)
            row = await cur.fetchone()
            await cur.close()
            cnx.close()
    return row


async def sqlexec(sql, values):
    """sql: exec values."""
    async with connections.pool.acquire() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(sql, values)
            await cnx.commit()
            last_rowid = cur.lastrowid
            await cur.close()
            cnx.close()
    return last_rowid


async def sqlcommit(sql):
    """sql: commit."""
    async with connections.pool.acquire() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(sql)
            await cnx.commit()
            rowcount = cur.rowcount
            await cur.close()
            cnx.close()
    return rowcount


async def sqlinsert(sql, values):
    """sql: insert values, user, password."""
    async with connections.pool.acquire() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(sql, values)
            await cnx.commit()
            last_rowid = cur.lastrowid
            await cur.close()
            cnx.close()
    return last_rowid


async def connect():
    host = 'localhost'
    port = 3310
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


connections = Connections()
