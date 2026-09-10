import sys
import tempfile
from pathlib import Path
import webview


def resource_path(relative: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / relative


def build_html() -> Path:
    parts_dir = resource_path("app_parts")
    html = "".join(p.read_text(encoding="utf-8") for p in sorted(parts_dir.glob("part*.txt")))
    replacements = {
        "assets/camera.webp": resource_path("assets/camera.webp").as_uri(),
        "assets/trio.webp": resource_path("assets/trio.webp").as_uri(),
        "assets/dexter.webp": resource_path("assets/dexter.webp").as_uri(),
        "assets/uno.png": resource_path("assets/uno.png").as_uri(),
        "assets/beach.webp": resource_path("assets/beach.webp").as_uri(),
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    target = Path(tempfile.mkdtemp(prefix="love_system_")) / "index.html"
    target.write_text(html, encoding="utf-8")
    return target


def main():
    webview.create_window(
        "love_system.exe — Luana + Yasmin",
        build_html().as_uri(),
        width=1540,
        height=920,
        min_size=(1120, 720),
        resizable=True,
        text_select=False,
        background_color="#070910",
    )
    webview.start(debug=False)


if __name__ == "__main__":
    main()
