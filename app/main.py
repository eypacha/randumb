from fastapi import FastAPI
from dotenv import load_dotenv
from app.config.resources import RESOURCES
from app.routes.generic import create_generic_router
from app.routes.health import router as health_router
from app.functions import generic_crud
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

openapi_tags = []
for resource_name, cfg in RESOURCES.items():
    openapi_tags.append(
        {
            "name": resource_name.capitalize(),
            "description": cfg.get("description", ""),
        }
    )

app = FastAPI(
    title="Randumb API",
    description="API for random dumb things",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

# Configure CORS (ALLOWED_ORIGINS env var, comma-separated, default="*")
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins_env.strip() == "*":
    allowed_origins = ["*"]
else:
    allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    generic_crud.init_tables(RESOURCES)


for resource, config in RESOURCES.items():
    router = create_generic_router(resource, config, generic_crud)
    app.include_router(router)

# include health routes (liveness/readiness)
app.include_router(health_router)
