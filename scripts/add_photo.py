"""Add a photo to the Gallery page.

Run it (double-click Add Photo.bat, or `python scripts/add_photo.py`),
answer the two prompts, then commit + push the changes.
"""

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GALLERY_DIR = ROOT / "assets" / "img" / "gallery"
PROFILE_PATH = ROOT / "content" / "profile.json"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def slugify(value):
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return value or "photo"


def unique_destination(directory, filename):
    stem, suffix = Path(filename).stem, Path(filename).suffix
    candidate = directory / f"{slugify(stem)}{suffix}"
    counter = 2
    while candidate.exists():
        candidate = directory / f"{slugify(stem)}-{counter}{suffix}"
        counter += 1
    return candidate


def main():
    source = input("Path to the photo file: ").strip().strip('"')
    source_path = Path(source).expanduser()

    if not source_path.is_file():
        print(f"Couldn't find a file at: {source_path}")
        sys.exit(1)

    if source_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        print(f"That's a {source_path.suffix} file. Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}")
        sys.exit(1)

    caption = input("Caption for this photo (optional, press Enter to skip): ").strip()

    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    destination = unique_destination(GALLERY_DIR, source_path.name)
    shutil.copy2(source_path, destination)

    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    image_path = destination.relative_to(ROOT).as_posix()
    entry = {"image": image_path}
    if caption:
        entry["title"] = caption
    profile["sections"]["gallery"].append(entry)
    PROFILE_PATH.write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nAdded {destination.name} to the gallery.")
    print("Next: commit and push (or ask Claude to do it) to publish it.")


if __name__ == "__main__":
    main()
