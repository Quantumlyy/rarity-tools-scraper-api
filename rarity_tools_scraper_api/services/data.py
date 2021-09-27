from fastapi import APIRouter, Path
from fastapi_cache.decorator import cache
from rarity_tools_scraper.data import Prices, get_collection_prices

router = APIRouter(prefix="/data", tags=["data.rarity.tools"])


@router.get("/prices/{collection_id}", response_model=Prices)
@cache(expire=60)
async def prices_collection(
    collection_id: str = Path(default="", description="ID of the desired collection")
) -> Prices:
    return get_collection_prices(collection_id)
