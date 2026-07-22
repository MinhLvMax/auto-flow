import re
import unicodedata


class TextNormalizer:

    def normalize(self, text: str) -> str:
        text = text.lower()

        text = unicodedata.normalize("NFD", text)
        text = "".join(
            c
            for c in text
            if unicodedata.category(c) != "Mn"
        )

        text = text.replace("đ", "d").replace("Đ", "D")

        text = re.sub(r"[^a-z0-9]+", " ", text)

        return re.sub(r"\s+", " ", text).strip()


if __name__ == '__main__':
    text_normalizer = TextNormalizer()
    text = fr'\\192.168.100.155\Socy Media\COUNTRY FOOTAGE\TÀU LINHTINH\an-old-train-travels-on-a-railway-laid-in-the-wate-2025-12-17-03-34-57-utc.mov'
    text_normalized = text_normalizer.normalize(text)
    print(text_normalized.split())
