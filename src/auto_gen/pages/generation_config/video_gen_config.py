from dataclasses import dataclass
from .base_generation_config import BaseGenerationConfig
from src.auto_gen.constant import VideoGenerationMode, VideoModelNameString

@dataclass
class VideoGenerationConfig(BaseGenerationConfig):
    generation_mode: VideoGenerationMode = VideoGenerationMode.INGREDIENTS
    model_name: str = VideoModelNameString.VEO_3_1_LITE_LOWER_PRIORITY
    duration: int = 8