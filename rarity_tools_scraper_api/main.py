import logging

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from rarity_tools_scraper_api.services import collectable, collections, data, projects

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("rest_api")

description = """
[![Donate with Ethereum](https://en.cryptobadges.io/badge/small/0xf82d0ea7A2eDde6d30cAf8A1E6Fed09f726fD584)](https://en.cryptobadges.io/donate/0xf82d0ea7A2eDde6d30cAf8A1E6Fed09f726fD584)

A simple API remapping internal [rarity.tools](https://rarity.tools) functions and methods into easy accessible REST endpoints.
"""

app = FastAPI(
    title="Rarity.tools scraping based API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Nejc Drobnič",
        "email": "nejc@drobnic.me",
        "url": "https://quantumly.dev",
    },
)


@app.on_event("startup")
async def on_startup():
    FastAPICache.init(InMemoryBackend())


app.include_router(collectable.router)
app.include_router(collections.router)
app.include_router(data.router)
app.include_router(projects.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
