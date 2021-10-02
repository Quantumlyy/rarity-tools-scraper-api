from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def set_chrome_options() -> Options:
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    chrome_prefs = dict()
    chrome_prefs["disk-cache-size"] = 4096
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_options.experimental_options["prefs"] = chrome_prefs

    return chrome_options


def block_google_cdn(driver: Chrome) -> None:
    driver.execute_cdp_cmd(
        "Network.setBlockedURLs",
        {
            "urls": [
                "https://lh3.googleusercontent.com",
                "https://projects.rarity.tools/static/images",
                "https://vultrobjects.com",
            ]
        },
    )
    driver.execute_cdp_cmd("Network.enable", {})


def init_driver() -> Chrome:
    driver = Chrome(
        options=set_chrome_options(),
        executable_path=r"C:\Users\Quantumly\Downloads\chromedriver_win32\chromedriver.exe",
    )
    block_google_cdn(driver)

    return driver
