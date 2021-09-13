from fastapi import APIRouter, Path
from fastapi_cache.decorator import cache
from rarity_tools_scraper.projects import Config, get_collection_config_static

router = APIRouter(
	prefix="/projects",
	tags=["projects.rarity.tools"]
)


@router.get(
	"/config/{collection_id}",
	response_model=Config
)
@cache(expire=60)
async def config_collection(
		collection_id: str = Path(default="", description="ID of the desired collection")
) -> Config:
	return get_collection_config_static(collection_id)
