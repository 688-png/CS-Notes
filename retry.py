from pathlib import Path
from deep_translator import GoogleTranslator

files = [
    "notes/Java 虚拟机.md",
    "notes/Redis.md",
    "notes/缓存.md",
    "notes/MySQL.md",
    "notes/分布式.md",
    "notes/计算机操作系统 - 内存管理.md",
    "notes/计算机操作系统 - 死锁.md",
    "notes/集群.md"
]

translator = GoogleTranslator(source='auto', target='en')

for f in files:
    try:
        text = Path(f).read_text(encoding='utf-8')
        result = translator.translate(text[:4500])
        print(f"OK: {f}")
    except Exception as e:
        print(f"FAIL: {f} -> {e}")
