from fastapi import APIRouter, HTTPException
from app.schemas.pirate_insults import PirateInsult
from app.functions.pirate_insults import add_pirate_insult, get_random_pirate_insult, init_db
from typing import Dict

router = APIRouter(prefix="/pirate_insults", tags=["Pirate Insults"])

@router.on_event("startup")
def startup_event():
    init_db()

@router.post("/", response_model=Dict[str, int])
def create_pirate_insult(insult: PirateInsult):
    insult_id = add_pirate_insult(insult)
    return {"id": insult_id}

@router.get("/random", response_model=PirateInsult)
def get_random_insult():
    insult = get_random_pirate_insult()
    if not insult:
        raise HTTPException(status_code=404, detail="No pirate insults found.")
    return insult
