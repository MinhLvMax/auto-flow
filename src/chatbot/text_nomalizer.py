import re


class TextNormalizer:

    def __init__(self):
        self.char_map = self._build_char_map()

    def _build_char_map(self):
        groups = {
            "a": ["à", "á", "ả", "ã", "ạ", "ă", "â"],
            "d": ["đ"],
            "e": ["è", "é", "ẻ", "ẽ", "ẹ", "ê"],
            "i": ["ì", "í", "ỉ", "ĩ", "ị"],
            "o": ["ò", "ó", "ỏ", "õ", "ọ", "ô", "ơ"],
            "u": ["ù", "ú", "ủ", "ũ", "ụ", "ư"],
            "y": ["ỳ", "ý", "ỷ", "ỹ", "ỵ"]
        }

        result = {}

        for normal, chars in groups.items():
            for c in chars:
                result[c] = normal

        return result

    def normalize(self, text: str):
        text = text.lower()

        text = "".join(
            self.char_map.get(c, c)
            for c in text
        )

        text = re.sub(
            r"[_\-.]+",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()
