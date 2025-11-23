from src.main import app
__doc__ = """
Тест выгрузки больших данных через EventSource
и отображении их пользаку

Файл нужен чтоб uvicorn не ругался 'src/main:app'

uvicorn --host 127.0.0.2 --port 8080 --env-file ./.env asgi:app
"""