from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import sqlite3
from app.functions import generic_crud

router = APIRouter()


@router.get("/health", summary="Liveness probe", description="Simple liveness check.")
def health():
    return {"status": "ok"}


@router.get(
    "/ready",
    summary="Readiness probe",
    description="Checks database connectivity and readiness.",
)
def readiness():
    try:
        # Attempt to open a connection and run a simple query
        conn = sqlite3.connect(generic_crud.DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        _ = cur.fetchone()
        conn.close()
        return {"status": "ready"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "reason": str(e)},
        )
