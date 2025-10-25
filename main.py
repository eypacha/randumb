from fastapi import FastAPI
from app.routes import pirates

app = FastAPI(title="Randumb API", description="API for random dumb things", version="0.1.0")

app.include_router(pirates.router)
