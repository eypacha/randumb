from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel
from uuid import UUID
from typing import List
import os


def create_generic_router(resource_name: str, config: dict, crud):
    router = APIRouter(prefix=f"/{resource_name}", tags=[resource_name.capitalize()])

    class ItemCreate(BaseModel):
        text: str
        lang: str

    class ItemOut(BaseModel):
        id: UUID
        text: str
        lang: str

    class PaginatedList(BaseModel):
        items: List[ItemOut]
        total: int
        page: int
        limit: int
        total_pages: int

    plural = config.get("plural", f"{resource_name} items")
    singular = config.get("singular", f"{resource_name} item")

    @router.get(
        "/random",
        response_model=ItemOut,
        summary=f"Get a random {singular}",
        description=f"Returns a single random {singular}. Optionally filter by language with ?lang=xx",
    )
    def get_random_item(
        lang: str = Query(None, description="Optional language code to filter by")
    ):
        try:
            item = crud.get_random_item(resource_name, lang)
            if not item:
                raise HTTPException(status_code=404, detail="No items found.")
            return item
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get(
        "/{lang}",
        response_model=PaginatedList,
        summary=f"List {plural}",
        description=f"Lists {plural} by language with pagination.",
    )
    def list_items_by_lang(
        lang: str = Path(...),
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
    ):
        try:
            return crud.list_items_by_lang(resource_name, lang, page, limit)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get(
        "/random",
        response_model=ItemOut,
        summary=f"Get a random {singular}",
        description=f"Returns a single random {singular}. Optionally filter by language with ?lang=xx",
    )
    def get_random_item(
        lang: str = Query(None, description="Optional language code to filter by")
    ):
        try:
            item = crud.get_random_item(resource_name, lang)
            if not item:
                raise HTTPException(status_code=404, detail="No items found.")
            return item
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    if os.getenv("ENABLE_CREATE", "true").lower() == "true":

        @router.post(
            "/",
            response_model=ItemOut,
            summary=f"Create a new {singular}",
            description=f"Creates a new {singular} in the {resource_name} resource.",
        )
        def create_item(item: ItemCreate):
            try:
                return crud.create_item(resource_name, item)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    if os.getenv("ENABLE_DELETE", "true").lower() == "true":

        @router.delete(
            "/{id}",
            status_code=204,
            summary=f"Delete a {singular}",
            description=f"Deletes a {singular} from the {resource_name} resource by ID.",
        )
        def delete_item(id: UUID = Path(...)):
            try:
                deleted = crud.delete_item(resource_name, str(id))
                if not deleted:
                    raise HTTPException(status_code=404, detail="Item not found.")
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    return router
