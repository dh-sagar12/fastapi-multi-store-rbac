from fastapi import FastAPI


app = FastAPI(
    title='Admin-Beniya SmartMart Mangement',
    version='1.0',
    servers=[{
        'url': 'http://localhost:8001'
    }]
)