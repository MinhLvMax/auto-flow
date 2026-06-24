
from playwright.sync_api import sync_playwright, TimeoutError, Locator, Error
from playwright.sync_api._generated import Page
from src.auto_flow.config import CHATGPT_PROFILE
from src.auto_flow.utils.helpers import debug_locator
from playwright.sync_api import sync_playwright

CHATGPT_URL = "https://chatgpt.com/"

def single_chat(input: str):
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=CHATGPT_PROFILE,
            headless=False,
            channel="chrome",
        )
        page = context.new_page()
        page.goto(CHATGPT_URL)
        input_entry = page.get_by_role("textbox", name="Chat with ChatGPT")
        input_entry.fill(input)
        page.wait_for_timeout(10000)
        sendbtn = page.get_by_test_id("send-button")
        sendbtn.click()
        text_output = page.locator('div > p')
        debug_locator(text_output)
        page.pause()

if __name__ == '__main__':
    single_chat("Xin chào")

