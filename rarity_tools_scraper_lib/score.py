from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_COLLECTABLE_VIEW_URL = "https://rarity.tools/{collection}/view/{id}"
ua = UserAgent()


def get_collectable_data(driver: webdriver.Chrome, collection: str, collectable: str):
	driver.get(BASE_COLLECTABLE_VIEW_URL.format(collection=collection, id=collectable))

	new_tab = driver.window_handles[-1]
	driver.switch_to.window(new_tab)

	try:
		element = WebDriverWait(driver, 120)\
			.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".font-extrabold.text-green-500")))
	finally:
		driver.close()

	return element
