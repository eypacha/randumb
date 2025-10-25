from fastapi import APIRouter, HTTPException
from app.schemas.pirates import Pirate
from app.functions.pirates import add_pirate, init_db, get_all_pirates
from typing import Dict

router = APIRouter(prefix="/pirates", tags=["Pirates insults"])

@router.on_event("startup")
def startup_event():
    init_db()

@router.post("/", response_model=Dict[str, int], summary="Create a pirate insult", description="Add a new pirate insult to the database.")
def create_pirate(pirate: Pirate):
    pirate_id = add_pirate(pirate)
    return {"id": pirate_id}


@router.get("/", response_model=list[Pirate], summary="List pirate insults", description="Get all pirate insults from the database.")
def list_pirates():
    return get_all_pirates()


