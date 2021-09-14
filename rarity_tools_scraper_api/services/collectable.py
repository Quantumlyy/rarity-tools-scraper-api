from fastapi import APIRouter, Path
from fastapi_cache.decorator import cache
from selenium import webdriver

from rarity_tools_scraper_lib.chrome import set_chrome_options, block_google_cdn
from rarity_tools_scraper_lib.score import get_collectable_data

# TODO: https://sqa.stackexchange.com/questions/45933/how-do-i-enable-chromedriver-to-use-browser-cache-or-local-storage-with-selenium
driver = webdriver.Chrome(options=set_chrome_options(),
                          executable_path=r"C:\Users\Quantumly\Downloads\chromedriver_win32\chromedriver.exe")
block_google_cdn(driver)

driver.get("https://google.com")

router = APIRouter(
    prefix="/collectable"
)


@router.get(
    "/score/{collection_id}/{collectable_id}"
)
@cache(expire=60 * 60 * 24)
async def collectable_score(
        collection_id: str = Path(default="", description="ID of the desired collection"),
        collectable_id: str = Path(default="", description="ID of the desired collectable")
) -> str:
	return get_collectable_data(driver, collection_id, collectable_id).text
