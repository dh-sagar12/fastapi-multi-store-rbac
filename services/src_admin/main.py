from fastapi import FastAPI


app = FastAPI(
    title="Admin-HamroMart SmartMart Mangement",
    version="1.0",
    servers=[{"url": "http://localhost:8000"}],
)
