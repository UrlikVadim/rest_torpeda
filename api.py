__doc__= """
API
"""
import os
import logging
from datetime import datetime
from contextlib import asynccontextmanager

import psycopg_pool
import valkey.asyncio
from fastapi import APIRouter
from pydantic import BaseModel

log = logging.getLogger("api")

MAX_CONN_POOLS = os.environ.get("MAX_CONN_POOLS")

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

class LargeTableRow(BaseModel):
    id: int
    text_f: str
    number_f: int
    ts_f: datetime
    bool_f: bool

router = APIRouter(prefix="/api/v1")

