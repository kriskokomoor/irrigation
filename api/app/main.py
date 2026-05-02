from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from .routes import zones
from .config import ESP32_BASE_URL


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info(f"CONFIG ESP32_BASE_URL = {ESP32_BASE_URL}")
    yield
    # optional shutdown logic here


app = FastAPI(lifespan=lifespan)

app.include_router(zones.router)