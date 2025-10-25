from fastapi import APIRouter, HTTPException
from app.schemas.pirates import Pirate
from app.functions.pirates import add_pirate, init_db, get_all_pirates
from typing import Dict

router = APIRouter(prefix="/pirates", tags=["Pirates"])

@router.on_event("startup")
def startup_event():
    init_db()

@router.post("/", response_model=Dict[str, int])
def create_pirate(pirate: Pirate):
    pirate_id = add_pirate(pirate)
    return {"id": pirate_id}


@router.get("/", response_model=list[Pirate])
def list_pirates():
    return get_all_pirates()


