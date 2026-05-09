from fastapi import FastAPI

from .router import router

app = FastAPI(title="Analyze Claim API")
app.include_router(router)
