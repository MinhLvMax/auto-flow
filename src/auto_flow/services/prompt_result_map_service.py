# Bạn tự sửa import theo project của bạn
# from ... import PromptResultStatus
# from ... import PromptResultType


class PromptResultMapService:
    def __init__(self, data: dict):
        self.map = {}
        self.build_map(data)

    def build_map(self, data: dict):
        self.map = {}
        self._scan(data)
        return self.map

    def _scan(self, data):
        if isinstance(data, dict):
            if "sentence" in data and "type" in data:
                sentence = data["sentence"]
                prompt_type = PromptResultType(data["type"])
                status = PromptResultStatus(data.get("status", "pending"))

                if sentence not in self.map:
                    self.map[sentence] = []

                self.map[sentence].append({
                    "type": prompt_type,
                    "status": status,
                })

            for item in data.get("prompts", []):
                self._scan(item)

        elif isinstance(data, list):
            for item in data:
                self._scan(item)

    def get_by_sentence(self, sentence: str):
        return self.map.get(sentence, [])

    def get_image_status(self, sentence: str):
        return self._get_status(sentence, PromptResultType.IMAGE)

    def get_video_status(self, sentence: str):
        return self._get_status(sentence, PromptResultType.VIDEO)

    def _get_status(self, sentence: str, prompt_type: PromptResultType):
        items = self.get_by_sentence(sentence)

        for item in items:
            if item["type"] == prompt_type:
                return item["status"]

        return PromptResultStatus.PENDING