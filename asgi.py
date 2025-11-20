__doc__ = """

Тест выгрузки больших данных через EventSource
и отображении их пользаку

uvicorn --host 127.0.0.1 --port 8080 asgi:app --reload
"""
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/")
async def index():
    return FileResponse("dist/index.html")


app.mount("/", StaticFiles(directory="dist"), name="dist")