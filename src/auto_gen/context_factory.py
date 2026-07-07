from playwright.sync_api import sync_playwright

class ContextFactory:
    def __init__(self):
        self.playwright = sync_playwright().start()

    def create_context(self, user_profile, download_path):
        return self.playwright.chromium.launch_persistent_context(
            user_data_dir=user_profile,
            headless=False,
            channel="chrome",
            accept_downloads=True,
            downloads_path=download_path
        )

    def close(self):
        self.playwright.stop()