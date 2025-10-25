from fastapi import FastAPI
from dotenv import load_dotenv
from app.config.resources import RESOURCES
from app.routes.generic import create_generic_router
from app.functions import generic_crud

load_dotenv()

app = FastAPI(
    title="Randumb API", description="API for random dumb things", version="0.1.0"
)


@app.on_event("startup")
def startup_event():
    generic_crud.init_tables(RESOURCES)


for resource, config in RESOURCES.items():
    router = create_generic_router(resource, config, generic_crud)
    app.include_router(router)
