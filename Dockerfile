FROM debian:13
RUN apt update
WORKDIR /app
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt
CMD uvicorn server:app -w 1 --host 0.0.0.0 --port 8080