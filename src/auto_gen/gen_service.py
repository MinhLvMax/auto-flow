from src.auto_gen.pages.google_flow_page import GoogleFlowPage
from src.auto_gen.json_reader import JsonReader
from src.auto_gen.json_writer import JsonWriter
from src.auto_gen.constant import GenMode
from src.auto_gen.pages.generation_config import ImageGenerationConfig, VideoGenerationConfig
from pathlib import Path
import time
import random


class GenService:
    def __init__(self, google_flow_page_obj: GoogleFlowPage):
        self.google_flow_page_obj = google_flow_page_obj
        # Các đối tượng đọc ghi
        self.reader = JsonReader()
        self.writer = JsonWriter()

    def run_prompt_file(self, prompt_path: Path):
        self.google_flow_page_obj.go_to_this_page()
        self.google_flow_page_obj.create_with_google_flow()

        prj_page = self.google_flow_page_obj.get_or_create_new_project(prompt_path.stem)

        data = self.reader.read(path=prompt_path)

        start = time.time()
        for i, pair in enumerate(data):
            print(f'Cặp thứ {i}/{len(data)}')
            if pair.get("image_done"):
                print("skip image")
            else:
                prj_page.send_a_prompt(
                    pair.get('image'),
                    GenMode.IMAGE,
                    ImageGenerationConfig()
                )
                prj_page.wait_until_creating_image_below(1)
                pair["image_done"] = True

            if pair.get("video_done"):
                print("skip video")
            else:
                prj_page.create_video_from_latest_image(
                    pair.get('video'),
                    VideoGenerationConfig()
                )
                pair["video_done"] = True
                prj_page.wait_until_creating_video_below(1)

            print('Lưu trạng thái gen')
            self.writer.write(prompt_path, data)

            print('Nghỉ 1 chút')
            prj_page.wait_for_seconds(random.randint(5, 10))

        end = time.time()
        print(f"Thời gian chạy: {end - start:.2f} giây")

    def run_prompt_folder(self, prompt_folder_path):
        prompt_folder_path = self._get_prompt_files(prompt_folder_path)
        for prompt_file_path in prompt_folder_path:
            self.run_prompt_file(prompt_file_path)
        pass

    def _get_prompt_files(self, prompt_folder: Path) -> list[Path]:
        return sorted(
            file
            for file in prompt_folder.glob("*.json")
            if file.is_file()
        )


if __name__ == '__main__':
    g = GenService()
    print(g._get_prompt_files(Path(r'D:\projects\auto-flow\src\auto_gen\input')))
