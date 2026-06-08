from pathlib import Path
from deep_translator import GoogleTranslator
import time

translator = GoogleTranslator(source='auto', target='en')

for md in Path(".").rglob("*.md"):
    try:
        print(f"Translating: {md}")

        text = md.read_text(encoding="utf-8", errors="ignore")

        if len(text.strip()) < 10:
            continue

        chunks = [text[i:i+3000] for i in range(0, len(text), 3000)]
        translated = ""

        for chunk in chunks:
            translated += translator.translate(chunk) + "\n"
            time.sleep(0.5)

        md.write_text(translated, encoding="utf-8")

    except Exception as e:
        print(f"Failed: {md} -> {e}")
