import time
import logging
from fastapi import FastAPI, Request

from .router import router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Analyze Claim API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(
        f"Type: {request.method} | Route: {request.url.path} | Duration: {duration:.4f}s"
    )
    return response

app.include_router(router)
