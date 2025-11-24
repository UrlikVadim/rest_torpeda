__doc__= """
API
"""
import os
import uuid
import json
import asyncio
import logging
from datetime import datetime
from contextlib import asynccontextmanager

import valkey
import valkey.client
import valkey.asyncio
import psycopg_pool
from psycopg import rows
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sse_starlette import ServerSentEvent
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

log = logging.getLogger("api")

DB_POOL = psycopg_pool.AsyncConnectionPool(
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


CACHE_POOL = AsyncValkeyConnectionPool(
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
    async with DB_POOL.connection() as conn:
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
            async with CACHE_POOL.connection() as dict_server:
                event = {
                    "event": "insert",
                    "data": params
                }
                data = await dict_server.publish(EVENT_CHANNEL, jsonable_encoder(event))
                return JSONResponse({"message": "Запись добавлена"})


@router.patch("/{row_id}")
async def create(row_id: int, row: LargeTableRow):
    """
    Обновляем запись в бд и оповещаем по каналу редис(valkey)
    """
    async with DB_POOL.connection() as conn:
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
            async with CACHE_POOL.connection() as dict_server:
                event = {
                    "event": "update",
                    "data": params
                }
                data = await dict_server.publish(EVENT_CHANNEL, jsonable_encoder(event))
                return JSONResponse({"message": "Запись обновлена"})


@router.delete("/{row_id}")
async def create(row_id: int):
    """
    Обновляем запись в бд и оповещаем по каналу редис(valkey)
    """
    async with DB_POOL.connection() as conn:
        async with conn.cursor() as curs:
            sql = """
            DELETE FROM public.largetable
            WHERE id=%(id)s
            """
            params = {"id": row_id}
            await curs.execute(sql, params)
            await conn.commit()
            # Запись коммитнули теперь пуляем в канал редиски
            async with CACHE_POOL.connection() as dict_server:
                event = {
                    "event": "delete",
                    "data": params
                }
                data = await dict_server.publish(EVENT_CHANNEL, jsonable_encoder(event))
                return JSONResponse({"message": "Запись обновлена"})

@router.get("/")
async def stream(request: Request):
    return ServerSentEvent(StreamLargeTable(request))


class DataEnd(Exception):
    """
    Исключение бросается когда нет больше данных для выгрузки пользователю
    """

class StreamLargeTable:
    active_connections = 0

    def __init__(self, request: Request, chunk_size:int=1000):
        self.uuid = uuid.uuid4().hex
        self.chunk_size = chunk_size
        self.request = request
        self.start_time = datetime.now()

    def __str__(self):
        return f"[STREAM ({self.active_connections} active PID: {os.getpid()}) UUID: {self.uuid} {datetime.now() - self.start_time} alive]"
    
    async def __aiter__(self):
        """
        Оборачиваем поток в трай чтоб при ошибке js EventSource не переподключался
        """
        self.__class__.active_connections += 1
        log.info(f"{self} старт")
        try:
            async for data in self.stream():
                yield data
        except Exception as e:
            log.error(f"{self} ошибка", exc_info=True)
            if not (await self.request.is_disconnected()):
                yield {
                    "event": "error",
                    "data": jsonable_encoder({"message": f"Ошибка {type(e)} в потоке {self}"})
                }
                log.info(f"{self} Отправил пользователю событие об ошибке")
        self.__class__.active_connections -= 1
        log.info(f"{self} конец")

    async def stream(self):
        """
        основная гена для выгрузки данных и обработки событий
        """
        max_id = 0
        # Для начала выгрузим сколько всего строк в бд
        async with DB_POOL.connection() as conn:
            async with conn.cursor(row_factory=rows.dict_row) as curs:
                sql = """
                SELECT 
                    count(*) as row_count,
                    max(id) as max_id
                FROM public.largetable
                """
                await curs.execute(sql)
                meta = await curs.fetchone()
                max_id = meta["max_id"]
                yield {
                    "event": "store_info",
                    "data": jsonable_encoder(meta)
                }
                log.info(f"{self} Выгрузил мета инфу: {meta['row_count']} всего строк в таблице. {max_id=}")
        
        # Затем подписываемся на valkey (коннект не блокируем)
        async with CACHE_POOL.connection() as conn_valkey:
            subscriber = conn_valkey.pubsub()
        async with subscriber as channel:
            res = await channel.subscribe(EVENT_CHANNEL)
            log.debug(f"{self} подписался на канал сообщений {res}")

            # max_id+1 так как при начале выгрузки зацепить новую строчку
            last_id = self.request.headers.get("Last-Event-ID", max_id+1) 
            # Флаг выгрузки данныз пользователю 
            downloaded = False 

            while not (await self.request.is_disconnected()):
                # Тут выгружаем данные из таблицы (или кэш)
                if not downloaded:
                    try:
                        async for row in self.storage(last_id):
                            yield {
                                "data": jsonable_encoder(row),
                                "id": str(row["id"])
                            }
                            last_id = row["id"]
                    except DataEnd:
                        downloaded = True
                        # Отправим событие что все выгрузили
                        yield {
                            "event": "store_end",
                            "data": jsonable_encoder({"time": str(datetime.now() - self.start_time)})
                        }
                        log.info(f"{self} ВЫГРУЗИЛ ВСЕ ДАННЫЕ")
                else:
                    # Все выгрузили - можно и поспать (не отключаем а слушаем PUBSUB на изменение данных)
                    await asyncio.sleep(1)
                
                # Тут чекаем pubsub на наличие событий изменивших какую либо строку 
                message = await channel.get_message(ignore_subscribe_messages=True, timeout=None)
                if message is not None:
                    # Полученый жисон в байтах нужно преобразовать в словарь для EventSource starlette + залогируем
                    data = json.loads(message["data"])
                    yield {
                        "event": data["event"],
                        "data": jsonable_encoder(data["data"])
                    }
                    log.info(f"{self} Событие {data['event']} id: {data['data']}")
            else:
                log.info(f"{self} Пользователь отключился")


    async def storage(self, last_id: int):
        """
        гена для выгрузки строк чанком из БД
        (в будущем можно будет прикрутить кэш)
        """
        async with DB_POOL.connection() as conn:
            async with conn.cursor(row_factory=rows.dict_row) as curs:
                sql = """
                SELECT 
                    id,
                    text_f,
                    number_f,
                    ts_f,
                    bool_f
                FROM public.largetable 
                WHERE id < %s
                ORDER BY id DESC
                LIMIT %s
                """
                await curs.execute(sql, (last_id, self.chunk_size))

                async for r in curs:
                    r["row_info"] = "Выгружена с БД"
                    yield r
                
                # Если выгребли меньше чанка - значит данные в бд закончились
                if curs.rowcount < self.chunk_size:
                    log.debug(f"{self} данные из бд закончились")
                    raise DataEnd()