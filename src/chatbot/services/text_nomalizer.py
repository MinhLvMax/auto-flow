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

    def tokenize(self, text: str) -> list[str]:
        text_normalized = self.normalize(text)
        return text_normalized.split()

if __name__ == '__main__':
    text_normalizer = TextNormalizer()
    text = fr'\\\\192.168.100.155\\Socy Media\\COUNTRY FOOTAGE\\Viet Nam\\chap 07-Cầu kính Bạch Long – Việt Nam\\Cầu Kính Bạch Long-Mộc Châu, Sơn La   Bach Long Glass Bridge-Moc Chau, Son La_converted.mp4'
    text_normalized = text_normalizer.normalize(text)
    print(text_normalized)
    print(text_normalized.split())
