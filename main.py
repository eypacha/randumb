from fastapi import FastAPI
from app.routes import pirates

app = FastAPI(title="Randumb API", description="API para cosas idiotas al azar", version="0.1.0")

app.include_router(pirates.router)
