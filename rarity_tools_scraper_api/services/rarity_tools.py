from fastapi import APIRouter, Path, Depends
from fastapi_cache.decorator import cache
from rarity_tools_scraper.collections import Collections, get_all_collections
from rarity_tools_scraper.data import get_collection_prices, Prices
from rarity_tools_scraper.projects import (
    StaticData,
    Config,
    get_collection_config_static,
    get_collection_staticdata_static,
)
from sqlalchemy.orm import Session

from rarity_tools_scraper_data import models
from rarity_tools_scraper_data.database import get_db
from rarity_tools_scraper_lib.data import (
    generate_collection_string,
    handle_collectable_data,
)
from rarity_tools_scraper_lib.structures import Collectable

router = APIRouter(prefix="/rt", tags=["rarity.tools"])


@router.get(
    "/collection/all",
    description="Returns an object containing a list of all available collections and their metadata.",
    response_model=Collections,
)
@cache(expire=60 * 60)
async def collections_all() -> Collections:
    return get_all_collections()


@router.get(
    "/{collection_id}/prices",
    description="Returns a list of all indexed prices for the target collection.",
    response_model=Prices,
)
@cache(expire=60)
async def collection_prices(
    collection_id: str = Path(default="", description="Name of the target collection.")
) -> Prices:
    return get_collection_prices(collection_id)


@router.get(
    "/{collection_id}/config",
    description="Returns the website config of the target collection.",
    response_model=Config,
)
@cache(expire=60)
async def config_collection(
    collection_id: str = Path(default="", description="Name of the target collection.")
) -> Config:
    return get_collection_config_static(collection_id)


@router.get(
    "/{collection_id}/staticdata",
    description="Returns all the static ranking data needed to calculate the score of entries in the target collection.",
    response_model=StaticData,
)
@cache(expire=60 * 60)
async def staticdata_collection(
    collection_id: str = Path(default="", description="Name of the target collection.")
) -> StaticData:
    return get_collection_staticdata_static(collection_id)


@router.get("{collection_id}/{collectable_id}/ranking", response_model=Collectable)
@cache(expire=60 * 60 * 24)
async def collectable_score(
    collection_id: str = Path(default="", description="Name of the target collection."),
    collectable_id: str = Path(
        default="", description="ID of the target collectable or item."
    ),
    db: Session = Depends(get_db),
) -> str:
    collectable = (
        db.query(models.Collectable)
        .filter(
            models.Collectable.id
            == generate_collection_string(collection_id, collectable_id)
        )
        .first()
    )

    if collectable is None or collectable.stale is True:
        score, rank = handle_collectable_data(collection_id, collectable_id)

        collectable = models.Collectable(
            id=generate_collection_string(collection_id, collectable_id),
            collection_id=collectable_id,
            collection_name=collection_id,
            score=float(score),
            rank=int(rank),
        )

        db.query(models.Collectable).filter(
            models.Collectable.id
            == generate_collection_string(collection_id, collectable_id)
        ).delete()

        db.add(collectable)
        db.commit()
        db.refresh(collectable)

    return Collectable(rank=int(collectable.rank), score=float(collectable.score))
