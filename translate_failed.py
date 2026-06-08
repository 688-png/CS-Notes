from pathlib import Path
from deep_translator import GoogleTranslator
import time

files = [
    "notes/Java 虚拟机.md",
    "notes/缓存.md",
    "notes/MySQL.md",
    "notes/分布式.md",
    "notes/计算机操作系统 - 内存管理.md",
    "notes/计算机操作系统 - 死锁.md"
]

translator = GoogleTranslator(source='auto', target='en')

for file in files:
    try:
        print(f"Translating {file}")

        text = Path(file).read_text(encoding="utf-8")

        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

        translated = ""

        for chunk in chunks:
            translated += translator.translate(chunk) + "\n"
            time.sleep(1)

        Path(file).write_text(translated, encoding="utf-8")

        print(f"SUCCESS: {file}")

    except Exception as e:
        print(f"FAILED: {file} -> {e}")
