"""Renderiza fuentes .puml usando el servidor oficial de PlantUML."""
import sys
import urllib.request
import zlib
from pathlib import Path

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


def encode3(value: int) -> str:
    return ALPHABET[value & 0x3F]


def encode6bit(data: bytes) -> str:
    out = []
    for index in range(0, len(data), 3):
        b1 = data[index]
        b2 = data[index + 1] if index + 1 < len(data) else 0
        b3 = data[index + 2] if index + 2 < len(data) else 0
        c1, c2 = b1 >> 2, ((b1 & 3) << 4) | (b2 >> 4)
        c3, c4 = ((b2 & 15) << 2) | (b3 >> 6), b3 & 63
        out.extend((encode3(c1), encode3(c2), encode3(c3), encode3(c4)))
    return "".join(out)


def render(source: Path) -> Path:
    compressed = zlib.compress(source.read_bytes(), 9)[2:-4]
    url = "https://www.plantuml.com/plantuml/png/" + encode6bit(compressed)
    target = source.with_suffix(".png")
    request = urllib.request.Request(url, headers={"User-Agent": "AutomatasPaint PlantUML renderer"})
    with urllib.request.urlopen(request, timeout=30) as response:
        target.write_bytes(response.read())
    if target.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        raise RuntimeError(f"PlantUML no devolvio un PNG para {source.name}")
    return target


if __name__ == "__main__":
    for argument in sys.argv[1:]:
        print(render(Path(argument)))
