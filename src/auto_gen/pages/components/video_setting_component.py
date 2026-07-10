import random
import re

from google.genai.types import VoiceConfig

from src.auto_gen.pages.components.base_component import BaseComponent
from src.auto_gen.constant import VideoModelNameString, RatiosMode, VideoGenerationMode
from playwright.sync_api import Page


class VideoSettingComponent(BaseComponent):
    def __init__(self, page):
        super().__init__(page)
        # Generation mode
        self.frames_mode = page.get_by_role("tab", name="crop_free Frames")
        self.ingrediens_mode = page.get_by_role("tab", name="chrome_extension Ingredients")

        # Ratios
        self.ratio_9_16 = page.get_by_role("tab", name="crop_9_16 9:")
        self.ratio_16_9 = page.get_by_role("tab", name="crop_16_9 16:")

        # Các nút chọn số lượng
        self.quantity_x1 = self.page.get_by_role("tab", name="1x")
        self.quantity_x2 = self.page.get_by_role("tab", name="x2")
        self.quantity_x3 = self.page.get_by_role("tab", name="x3")
        self.quantity_x4 = self.page.get_by_role("tab", name="x4")

        # Nút chọn model
        self.choose_model_btn = self.page.get_by_role(
            "button",
            name=re.compile(r"arrow_drop_down$")
        )

        # Các nút chọn thời lượng

    def _get_ratio_locator(self, ratio: RatiosMode):
        if ratio == RatiosMode.R_16_9:
            return self.ratio_16_9
        if ratio == RatiosMode.R_9_16:
            return self.ratio_9_16

    def _get_quantity_locator(self, quantity: int):
        if quantity == 1:
            return self.quantity_x1
        if quantity == 2:
            return self.quantity_x2
        if quantity == 3:
            return self.quantity_x3
        if quantity == 4:
            return self.quantity_x4

    def _get_video_generation_mode_locator(self, mode: VideoGenerationMode):
        if mode == VideoGenerationMode.FRAMES:
            return self.frames_mode
        elif mode == VideoGenerationMode.INGREDIENTS:
            return self.ingrediens_mode

    def configure(self, generator_mode: VideoGenerationMode, ratio: RatiosMode, quantity, model_name: VideoModelNameString, duration):
        # Tìm các nút
        generator_mode_locator = self._get_video_generation_mode_locator(generator_mode)
        ratio_locator = self._get_ratio_locator(ratio)
        quantity_locator = self._get_quantity_locator(quantity)
        self.choose_model_btn.click()
        list_model = ListVideoModelComponent(self.page)
        model_locator = list_model.get_model_locator_by_name(model_name)
        model_locator.click()
        # Cho các locator vào danh sách rồi xáo trộn lên rồi click
        self.click_random_order(generator_mode_locator, ratio_locator, quantity_locator)
        self.close_component()



class ListVideoModelComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.omni = page.get_by_role("button", name="volume_up Omni Flash")
        self.veo31lite = page.get_by_role("button", name="volume_up Veo 3.1 - Lite", exact=True)
        self.veo31fast = page.get_by_role("button", name="volume_up Veo 3.1 - Fast")
        self.veo31qual = page.get_by_role("button", name="volume_up Veo 3.1 - Quality")
        self.veo31litelower = page.get_by_role("button", name="volume_up Veo 3.1 - Lite [")

    def get_model_locator_by_name(self, model_name):
        if model_name == VideoModelNameString.OMNI_FLASH:
            return self.omni
        elif model_name == VideoModelNameString.VEO_3_1_LITE:
            return self.veo31lite
        elif model_name == VideoModelNameString.VEO_3_1_FAST:
            return self.veo31fast
        elif model_name == VideoModelNameString.VEO_3_1_QUALITY:
            return self.veo31qual
        elif model_name == VideoModelNameString.VEO_3_1_LITE_LOWER_PRIORITY:
            return self.veo31litelower