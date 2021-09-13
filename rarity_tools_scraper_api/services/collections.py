from fastapi import APIRouter
from fastapi_cache.decorator import cache
from rarity_tools_scraper.collections import Collections, get_all_collections

router = APIRouter(
	prefix="/collections"
)


@router.get(
	"/all",
	response_model=Collections
)
@cache(expire=60 * 60)
async def all_collections() -> Collections:
	return get_all_collections()
