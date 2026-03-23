import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query

from db import close_db, connect_db
from fids_service import handle_fids_down
from schemas import FidsResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    logger.info("FIDS Agentic Service started")
    yield
    await close_db()
    logger.info("FIDS Agentic Service stopped")


app = FastAPI(title="FIDS Agentic Service", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/fids/start", response_model=FidsResponse)
async def fids_down(ip: str = Query(..., description="IP address of the FIDS display")):
    try:
        result = await handle_fids_down(ip)
        return {
            "success": True,
            **result,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error handling FIDS down for IP %s", ip)
        raise HTTPException(status_code=500, detail="Internal server error")