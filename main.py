from fastapi import FastAPI
from routes import pirate_insults

app = FastAPI(title="Randumb API", description="API para cosas idiotas al azar", version="0.1.0")

app.include_router(pirate_insults.router)
