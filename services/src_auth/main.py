from fastapi import FastAPI, APIRouter

from libs.shared.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title='Beniya- SmartMart Management System',
    version='1.0',
    servers=[{
        'url': 'http://localhost:8001'
    }]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {'status': 'healthy'}
