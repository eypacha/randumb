import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi import Path, Query

load_dotenv()

from app.schemas.pirates import Pirate, PirateCreate, PirateLangOut, PirateLangOutSingle
from app.functions.pirates import (
    add_pirate,
    init_db,
    get_random_pirate,
    get_pirates_by_lang_paginated,
)

router = APIRouter(prefix="/pirates", tags=["Pirates insults"])


@router.on_event("startup")
def startup_event():
    init_db()


if os.getenv("ENABLE_CREATE_PIRATE", "true").lower() == "true":

    @router.post(
        "/",
        response_model=Pirate,
        summary="Create a pirate insult",
        description="Add a new pirate insult to the database.",
    )
    def create_pirate(pirate: PirateCreate):
        try:
            pirate_id = add_pirate(pirate)
            return Pirate(id=pirate_id, text=pirate.text, lang=pirate.lang)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error creating pirate insult: {e}"
            )


from pydantic import BaseModel


class PaginatedPirateList(BaseModel):
    items: list[PirateLangOut]
    total: int
    page: int
    limit: int
    total_pages: int


@router.get(
    "/{lang}",
    response_model=PaginatedPirateList,
    summary="List pirate insults by language",
    description="Get all pirate insults in the requested language, paginated.",
)
def list_pirates_by_lang(
    lang: str = Path(..., description="ISO code for language, e.g. 'en' or 'es'"),
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    limit: int = Query(10, ge=1, le=100, description="Results per page (max 100)"),
):
    try:
        items, total, page, limit, total_pages = get_pirates_by_lang_paginated(
            lang, page, limit
        )
        return PaginatedPirateList(
            items=items, total=total, page=page, limit=limit, total_pages=total_pages
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error listing pirate insults: {e}"
        )


@router.get(
    "/random/{lang}",
    response_model=PirateLangOutSingle,
    summary="Get a random pirate insult in a language",
    description="Retrieve a random pirate insult in the requested language from the database.",
)
def get_random_pirate_insult_lang(
    lang: str = Path(..., description="ISO code for language, e.g. 'en' or 'es'")
):
    try:
        pirate = get_random_pirate()
        if not pirate or pirate.lang != lang:
            raise HTTPException(
                status_code=404, detail="No pirate insults found for this language."
            )
        return PirateLangOutSingle(id=pirate.id, text=pirate.text, lang=pirate.lang)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting random pirate insult: {e}"
        )
