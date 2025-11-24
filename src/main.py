__doc__ = """
Основное asgi приложение
"""
import random
import logging
import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.api import DB_POOL, CACHE_POOL, router

logging.basicConfig(
    level=logging.INFO
)
log = logging.getLogger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await DB_POOL.open(wait=True)
    log.info("======= Старт ==================")
    yield
    log.info("======= Закрываю коннекты ======")
    await DB_POOL.close()
    await CACHE_POOL.aclose()
    log.info("======= Остановка ==============")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def index():
    return FileResponse("dist/index.html")

@app.get("/data")
async def count_data():
    """
    Считаем количество записей в БД
    """
    async with DB_POOL.connection() as conn:
        async with conn.cursor() as curs:
            sql = """
            SELECT count(*) FROM public.largetable
            """
            await curs.execute(sql)
            count = (await curs.fetchone())[0]
            return JSONResponse({"count": count})

@app.delete("/data")
async def delete_data():
    """
    Сносим таблицу
    """
    async with DB_POOL.connection() as conn:
        async with conn.cursor() as curs:
            sql = """
            TRUNCATE TABLE public.largetable
            """
            await curs.execute(sql)
            await conn.commit()
            return JSONResponse({"message": "Данные в БД удалены"})

class FillDataParams(BaseModel):
    count: int

@app.post("/data")
async def fill_data(params: FillDataParams):
    """
    Заполняем таблицу данными
    """
    async with DB_POOL.connection() as conn:
        async with conn.cursor() as curs:
            sql = """
            INSERT INTO public.largetable(text_f, number_f, ts_f, bool_f)
            VALUES (?, ?, ?, ?)
            """
            await curs.executemany(sql, (generate_row() for i in range(params.count)))
            count_insert_rows = curs.rowcount
            await conn.commit()
            return JSONResponse({"count": count_insert_rows})
        
app.include_router(router)

app.mount("/", StaticFiles(directory="dist"), name="dist")

# @app.exception_handler(Exception)
# async def error(request: Request, exc: Exception):
#     msg = f"Необработанная ошибка сервера (тип {type(exc)}) Код {uuid.uuid4().hex}" 
#     log.error(msg, exc_info=True)
#     return JSONResponse(
#         status_code=500,
#         content={"message": msg}
#     )

def generate_row():
    """
    Генерим случайную строку для занесения в БД
    """
    NOUNS = ["человек", "дом", "книга", "город", "машина", "ребенок", "собака", "кошка"]
    VERBS = ["делает", "смотрит", "читает", "строит", "ведет", "играет", "спит", "бежит"]
    ADJECTIVES = ["большой", "маленький", "новый", "старый", "красивый", "быстрый", "умный"]
    ADVERBS = ["быстро", "медленно", "громко", "тихо", "далеко", "близко"]
    adjective = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    verb = random.choice(VERBS)
    adverb = random.choice(ADVERBS)
    # Собираем предложение, делаем первую букву заглавной и ставим точку
    text_f = f"{adjective.capitalize()} {noun} {verb} {adverb}."
    number_f = random.randint(-999999, 999999)
    ts_f = datetime.datetime(
        year=random.randint(1970, 2077),
        month=random.randint(1, 12),
        day=random.randint(1, 28),
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
    )
    bool_f = random.choice((True, False, None))
    return (text_f, number_f, ts_f, bool_f)