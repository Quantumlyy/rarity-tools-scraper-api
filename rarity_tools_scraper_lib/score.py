from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from rarity_tools_scraper_lib.chrome import block_google_cdn, set_chrome_options

BASE_COLLECTABLE_VIEW_URL = "https://rarity.tools/{collection}/view/{id}"
ua = UserAgent()


def get_collectable_data(collection: str, collectable: str):
    # TODO: https://sqa.stackexchange.com/questions/45933/how-do-i-enable-chromedriver-to-use-browser-cache-or-local-storage-with-selenium
    driver = webdriver.Chrome(
        options=set_chrome_options(),
        # executable_path=r"C:\Users\Quantumly\Downloads\chromedriver_win32\chromedriver.exe"
    )
    block_google_cdn(driver)

    driver.get(BASE_COLLECTABLE_VIEW_URL.format(collection=collection, id=collectable))

    # new_tab = driver.window_handles[-1]
    # driver.switch_to.window(new_tab)

    element = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".font-extrabold.text-green-500")
        )
    )

    return element, driver
