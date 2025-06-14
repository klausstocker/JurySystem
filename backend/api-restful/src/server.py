"""server: db-api-fastapi."""
from __future__ import absolute_import
import uvicorn

__version__ = '1.0.0'

import decimal
import json
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException, status
from typing import Annotated, Union, Any
from fastapi import Depends, Query, Body
from pydantic import BaseModel

import db
from db import fetch, post_sql, post_json, post_form, sql_commit, sql_exec, sql_insert
# from flask import request
from flask import jsonify
from mediatypes import MediaTypes
import mysql.connector

description = """
🚀🚀 RESTful API 🚀🚀
"""

UnprivilegedException = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unprivileged user")
DisabledUserException = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Disabled user")

CredentialsException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                     detail="Could not validate credentials",
                                     headers={"WWW-Authenticate": "Bearer"})

UnauthorizedException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Incorrect username or password",
                                      headers={"WWW-Authenticate": "Bearer"},
                                      )

media_types = MediaTypes()


class Item(BaseModel):
    pass


@asynccontextmanager
async def lifespan(api: FastAPI):
    await db.connect()
    yield
    db.connections.pool.close()
    await db.connections.pool.wait_closed()


api = FastAPI(lifespan=lifespan,
              title="RESTful API",
              version="1.0.0",
              contact={"name": "Franz Krenn",
                       "email": "office@fkrenn.at"},
              summary="Simplify xour access",
              description=description)

api.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@api.get("/")
async def root() -> JSONResponse:
    """
    Handles the root GET request and returns a JSON response containing the status,
    message, and version information of the application. This endpoint serves as a
    health check or informational route for clients.
    """
    content = {'status': status.HTTP_200_OK, 'message': "OK", 'version': __version__}
    return JSONResponse(content=content, status_code=content.get('status'), media_type=media_types.APPLICATION_JSON)


@api.get("/api")
async def show_databases() -> JSONResponse:
    """
    Fetches and displays the list of all available databases from the server.

    This function executes a database query to fetch all the names of databases
    from the connected server. It sends a JSON response containing the list of
    database names to the client. The data is retrieved asynchronously.
    """
    query = "SHOW DATABASES"
    rows = await fetch(query, all=True)
    return JSONResponse(content=rows, status_code=status.HTTP_200_OK, media_type=media_types.APPLICATION_JSON)


@api.get("/api/{database}")
async def show_tables(database: str) -> JSONResponse:
    """
    Fetches and returns the list of tables from a specified database. This function executes
    a query to retrieve all tables from the provided database and returns the result as a
    JSON response with appropriate status code and media type.
    """
    query = f"SHOW TABLES FROM {database}"
    rows = await fetch(query, all=True)
    return JSONResponse(rows, status_code=status.HTTP_200_OK, media_type=media_types.APPLICATION_JSON)


@api.get("/api/{database}/{table}")
async def get_many(database: str, table: str,
                   fields: str = Query(description='fields', default=None),
                   limit: int = Query(gt=0, lt=10000, default=None)) -> JSONResponse:
    """
    Fetches multiple records from a specified database table or shows the table fields.

    This function is designed for querying records or table schema from a database, with optional
    support for selecting specific fields and limiting the number of records retrieved. The response
    is formatted as JSON. Depending on input parameters, it either queries data rows if fields are
    specified or shows table schema if fields are not specified.
    """
    query = f"SELECT {fields} FROM {database}.{table}" if fields else f"SHOW FIELDS FROM {database}.{table}"
    query = query + f" LIMIT {limit}" if limit and fields else query
    rows = await fetch(query, all=True)
    status_code = status.HTTP_200_OK if rows else status.HTTP_404_NOT_FOUND
    response_data = jsonable_encoder(rows) if rows else []
    return JSONResponse(response_data, status_code=status_code, media_type=media_types.APPLICATION_JSON)


@api.get("/api/{database}/{table}/{key}")
async def get_one(database: str, table: str, key: str,
                  column: str = Query(description='column', default='id'),
                  fields: str = Query(description='fields', default="*")) -> JSONResponse:
    """
    Handles HTTP GET requests to fetch a specific record from a database table based
    on a provided key. Supports specifying the column to search within and the fields
    to select in the response.
    """
    query = f"SELECT {fields} FROM {database}.{table} WHERE {column}='{key}'"
    row = await fetch(query)
    response_data = jsonable_encoder(row) if row else []
    status_code = status.HTTP_200_OK if row else status.HTTP_404_NOT_FOUND
    return JSONResponse(content=response_data, status_code=status_code, media_type=media_types.APPLICATION_JSON)


@api.post("/api")
async def post_api(request: Request):
    """POST: /api """
    content_type = request.headers.get('Content-Type')
    print(content_type)
    try:
        _json = await request.json()
    except Exception as e:
        print("TimeoutError", e)
        return JSONResponse(jsonable_encoder({"exception": e}), status_code=415, media_type="application/json")
    print(_json, request.headers)
    return JSONResponse([], status_code=415, media_type="application/json")
    if _json:
        return JSONResponse([], status_code=415, media_type="application/json")
        # return jsonify(status=415, post='json'), 415

    if request.form():
        return jsonify(status=415, post='form'), 415

    # if request.files():
    #    return jsonify(status=415, post='files'), 415

    if request.stream():
        content_type = request.headers.get('Content-Type')
        if content_type == 'image/jpg':
            return jsonify(status=415, post='stream', content_type='image/jpg'), 415

        if content_type == 'application/octet-stream':
            return jsonify(status=415,
                           post='stream',
                           content_type='application/octet-stream'), 415

        if str(content_type).lower().startswith('text/plain'):
            return jsonify(status=415, post='stream', content_type='text/plain'), 415

        if str(content_type).lower().startswith('text/sql'):
            return post_sql()

        return jsonify(status=415, post='stream'), 415

    return jsonify(status=415,
                   error='Unsupported Media Type',
                   method='POST'), 415


@api.post("/api/{database}/{table}")
async def post_insert(request: Request, item: Item, database=None, table=None):
    """
    Handles an HTTP POST request to insert a new row into the specified database and table. The
    method expects application/json as the Content-Type of the request. If valid JSON data
    is provided in the request body, it triggers an internal function for inserting the data.
    If the request does not meet this expectation, a structured error response is returned.
    """
    # Create a new row. key1=val1,key2=val2.
    content_type = request.headers.get('Content-Type')
    if content_type == media_types.APPLICATION_JSON:
        json_data = await request.json()
        if json_data:
            return await post_json(database, table, json_data)
    reply = {'status': status.HTTP_417_EXPECTATION_FAILED,
             'message': 'Expectation Failed',
             'details': 'Can Not Meet Expectation: request-header field',
             'method': 'POST',
             'insert': False}
    return JSONResponse(content=jsonable_encoder(reply), status_code=reply.get('status'),
                        media_type=media_types.APPLICATION_JSON)


@api.delete("/api/{database}/{table}/{key}")
async def delete_one(request: Request, database=None, table=None, key=None,
                     column: str = Query(description='column', default='id')):
    """
    Delete a single row from a specific table in a database by its primary key.
    This asynchronous function constructs and executes a SQL DELETE query to
    remove a specific record based on the provided key and optional column name.
    """
    # Delete a row by primary key id?column=
    query = f"DELETE FROM {database}.{table} WHERE {column}='{key}'"
    delete = await sql_commit(query) > 0
    reply = {'status': status.HTTP_200_OK if delete else status.HTTP_404_NOT_FOUND,
             'message': "Deleted" if delete else "Failed Delete",
             'delete': delete}
    return JSONResponse(content=jsonable_encoder(reply), status_code=reply.get('status'),
                        media_type=media_types.APPLICATION_JSON)


@api.patch("/api/{database}/{table}/{key}")
async def patch_one(request: Request, item: Item, database=None, table=None, key=None,
                    column: str = Query(description='column', default='id')) -> JSONResponse:
    """
    Updates a single row element in a specified database table based on the provided primary key. The function accepts a JSON body containing
    a single key-value pair to update. If the request contains content other than application/json or if an invalid payload
    is provided, the function responds with an appropriate error message. On successful update, the function returns a status of HTTP 201.
    """
    # Update row element by primary key (single key/val) id?column=
    reply = {"status": status.HTTP_412_PRECONDITION_FAILED}
    try:
        if request.headers['Content-Type'] == media_types.APPLICATION_JSON:
            json_data = await request.json()
            if len(json_data) > 1:
                reply = {'status': status.HTTP_405_METHOD_NOT_ALLOWED,
                         'errorType': 'Method Not Allowed',
                         'errorMessage': 'Single Key-Value Only',
                         'update': False}
            else:
                field, value = next(iter(json_data.items()))
                query = f"UPDATE {database}.{table} SET {field}='{value}' WHERE {column}='{key}'"
                update = await sql_commit(query) > 0
                reply = {'status': status.HTTP_201_CREATED if update else status.HTTP_404_NOT_FOUND,
                         'message': "Update" if update else "Failed Update",
                         'update': update}
        else:
            reply = {'status': status.HTTP_412_PRECONDITION_FAILED,
                     'errorType': 'Media Type not supported',
                     'errorMessage': 'Media Type Must Be application/json',
                     'update': False}
    except Exception as e:
        reply = {'status': status.HTTP_406_NOT_ACCEPTABLE,
                 'errorType': 'Update not successful',
                 'errorMessage': f'{e}',
                 'update': False}
    finally:
        return JSONResponse(content=jsonable_encoder(reply), status_code=reply.get('status'),
                            media_type=media_types.APPLICATION_JSON)


@api.put("/api/{database}/{table}")
async def put_replace(database=None, table=None):
    """PUT: /api/<database>/<table>."""
    # Replace existing row with new row. key1=val1,key2=val2."""
    database = request.view_args['database']
    table = request.view_args['table']

    if not request.headers['Content-Type'] == 'application/json':
        return jsonify(status=412, errorType="Precondition Failed"), 412

    post = request.get_json()

    placeholders = ['%s'] * len(post)

    fields = ",".join([str(key) for key in post])
    places = ",".join([str(key) for key in placeholders])

    records = []
    for key in post:
        records.append(post[key])

    sql = "REPLACE INTO " + database + "." + table
    sql += " (" + fields + ") VALUES (" + places + ")"

    replace = await sqlexec(sql, records)

    if replace > 0:
        return jsonify(status=201,
                       message="Created",
                       replace=True,
                       rowid=replace), 201

    return jsonify(status=461, message="Failed Create", replace=False), 461


def sql_connection(user=None, password=None):
    """sql: connection."""
    if not user:
        user = request.authorization.username

    if not password:
        password = request.authorization.password

    config = {
        'user': user,
        'password': password,
        'host': request.headers.get('X-Host', '127.0.0.1'),
        'port': int(request.headers.get('X-Port', '3306')),
        'database': request.headers.get('X-Db', ''),
        'raise_on_warnings': request.headers.get('X-Raise-Warnings', True),
        'get_warnings': request.headers.get('X-Get-Warnings', True),
        'auth_plugin': request.headers.get('X-Auth-Plugin', 'mysql_native_password'),
        'use_pure': request.headers.get('X-Pure', True),
        'use_unicode': request.headers.get('X-Unicode', True),
        'charset': request.headers.get('X-Charset', 'utf8'),
        'connection_timeout': int(request.headers.get('X-Connection-Timeout', 10)),
    }
    _db = mysql.connector.connect(**config)
    return _db


def main():
    """main: api."""
    uvicorn.run(api, host="0.0.0.0", port=5666)


if __name__ == '__main__':
    main()
