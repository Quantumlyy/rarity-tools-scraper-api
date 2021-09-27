from fastapi import APIRouter, Path
from fastapi_cache.decorator import cache
from selenium import webdriver

from rarity_tools_scraper_lib.chrome import set_chrome_options, block_google_cdn
from rarity_tools_scraper_lib.score import get_collectable_data


router = APIRouter(prefix="/collectable")


@router.get("/score/{collection_id}/{collectable_id}")
@cache(expire=60 * 60 * 24)
async def collectable_score(
    collection_id: str = Path(default="", description="ID of the desired collection"),
    collectable_id: str = Path(default="", description="ID of the desired collectable"),
) -> str:
    element, driver = get_collectable_data(collection_id, collectable_id)
    text = element.text
    driver.quit()

    return text
