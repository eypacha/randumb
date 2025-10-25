from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel
from uuid import UUID
from typing import List

# Este esqueleto asume que tendrás funciones CRUD genéricas en functions/generic_crud.py
# y que cada recurso tiene una tabla en la base de datos con los campos definidos en config/resources.py

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

    @router.post("/", response_model=ItemOut)
    def create_item(item: ItemCreate):
        try:
            return crud.create_item(resource_name, item)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/{lang}", response_model=PaginatedList)
    def list_items_by_lang(
        lang: str = Path(...),
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
    ):
        try:
            return crud.list_items_by_lang(resource_name, lang, page, limit)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.delete("/{id}", status_code=204)
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
