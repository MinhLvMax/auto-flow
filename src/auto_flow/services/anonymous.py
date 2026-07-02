import random
import time
from playwright.sync_api import Locator

class Anonymous:
    def random_wait_time_click(self, locator: Locator, min=1, max = 5):
        wait_time = random.randint(min, max)
        time.sleep(wait_time)
        locator.click()
        pass

    def random_wait_time_fill(self, locator: Locator, text, min=1, max = 5):
        wait_time = random.randint(min, max)
        time.sleep(wait_time)
        locator.fill(text)
        pass