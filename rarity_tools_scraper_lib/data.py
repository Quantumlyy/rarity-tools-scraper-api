from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from rarity_tools_scraper_lib.chrome import init_driver

BASE_COLLECTABLE_VIEW_URL = "https://rarity.tools/{collection}/view/{id}"
ua = UserAgent()


def get_collectable_data(
    collection: str, collectable: str, driver: webdriver.Chrome = None
):
    if driver is None:
        driver = init_driver()

    driver.get(BASE_COLLECTABLE_VIEW_URL.format(collection=collection, id=collectable))

    score_element = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".font-extrabold.text-green-500")
        )
    )
    rank_element = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".font-bold.whitespace-nowrap")
        )
    )

    return score_element, rank_element, driver
