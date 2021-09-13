import logging

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from rarity_tools_scraper_api.services import collections

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("rest_api")

app = FastAPI()


@app.on_event("startup")
async def on_startup():
	FastAPICache.init(InMemoryBackend())

app.include_router(collections.router)

if __name__ == "__main__":
	uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
