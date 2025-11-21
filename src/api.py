__doc__= """
API
"""
import os
import logging
from datetime import datetime
from contextlib import asynccontextmanager

import psycopg_pool
import valkey
import valkey.client
import valkey.asyncio
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

log = logging.getLogger("api")

POSTGRES_POOL = psycopg_pool.AsyncConnectionPool(
    kwargs={
        "host": os.environ["DB_HOST"],
        "database": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
    },
    min_size=1,
    max_size=os.environ["DB_MAX_CONN"],
    open=False
)

class AsyncValkeyConnectionPool(valkey.asyncio.BlockingConnectionPool):
    """
    Унаследовал так как пул не имеет менеджера контекста
    (по примеру постгре пула)
    """
    @asynccontextmanager
    async def connection(self):
        conn = await self.get_connection()
        try:
            yield conn
        finally:
            await self.release(conn)

VALKEY_POOL = AsyncValkeyConnectionPool(
    connection_kwargs={
        "host": os.environ["DICT_SERVER_HOST"]
    },
    max_connections=os.environ["DICT_SERVER_MAX_CONN"]
)

EVENT_CHANNEL = "event-public.largetable"

class LargeTableRow(BaseModel):
    text_f: str
    number_f: int
    ts_f: datetime
    bool_f: bool

router = APIRouter(prefix="/api/v1")

@router.post("/")
async def create(row: LargeTableRow):
    """
    Создаем запись в бд и оповещаем по каналу редис(valkey)
    """
    async with POSTGRES_POOL.connection() as conn:
        async with conn.cursor() as curs:
            sql = """
            INSERT INTO public.largetable(text_f, number_f, ts_f, bool_f)
            VALUES (%(text_f)s, %(number_f)s, %(ts_f)s, %(bool_f)s)
            RETURNING id
            """
            params = row.model_dump()
            await curs.execute(sql, params)
            params["id"] = await curs.fetchone()[0]
            await conn.commit()
            # Запись коммитнули теперь пуляем в канал редиски
            async with VALKEY_POOL.connection() as dict_server:
                event = {
                    "event": "insert",
                    "data": params
                }
                await dict_server.publish(EVENT_CHANNEL, jsonable_encoder(event))
            return JSONResponse({"message": "Запись добавлена"})
        
@router.put("/{row_id}")
async def create(row_id: int, row: LargeTableRow):
    """
    Обновляем запись в бд и оповещаем по каналу редис(valkey)
    """
    async with POSTGRES_POOL.connection() as conn:
        async with conn.cursor() as curs:
            sql = """
            UPDATE public.largetable
            SET text_f=%(text_f)s, number_f=%(number_f)s, ts_f=%(ts_f)s, bool_f=%(bool_f)s
            WHERE id=%(id)s
            """
            params = row.model_dump()
            params["id"] = row_id
            await curs.execute(sql, params)
            await conn.commit()
            # Запись коммитнули теперь пуляем в канал редиски
            async with VALKEY_POOL.connection() as dict_server:
                event = {
                    "event": "update",
                    "data": params
                }
                await dict_server.publish(EVENT_CHANNEL, jsonable_encoder(event))
            return JSONResponse({"message": "Запись обновлена"})

@router.delete("/{row_id}")
async def create(row_id: int):
    """
    Обновляем запись в бд и оповещаем по каналу редис(valkey)
    """
    async with POSTGRES_POOL.connection() as conn:
        async with conn.cursor() as curs:
            sql = """
            DELETE FROM public.largetable
            WHERE id=%(id)s
            """
            params = {"id": row_id}
            await curs.execute(sql, params)
            await conn.commit()
            # Запись коммитнули теперь пуляем в канал редиски
            async with VALKEY_POOL.connection() as dict_server:
                event = {
                    "event": "delete",
                    "data": params
                }
                await dict_server.publish(EVENT_CHANNEL, jsonable_encoder(event))
            return JSONResponse({"message": "Запись обновлена"})