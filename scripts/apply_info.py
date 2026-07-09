"""Apply content/my-info.txt to content/profile.json.

Run it (double-click Update My Info.bat, or `python scripts/apply_info.py`)
after editing content/my-info.txt. It only touches your bio, stats,
skills, highlights, projects, experience, and education — Gallery photos
and Blog posts are still managed by their own scripts.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INFO_PATH = ROOT / "content" / "my-info.txt"
PROFILE_PATH = ROOT / "content" / "profile.json"

SECTION_HEADER = re.compile(r"^===\s*(.+?)\s*===$")


def parse_kv(line):
    if ":" not in line:
        return None
    key, _, value = line.partition(":")
    return key.strip().upper(), value.strip()


def split_blocks(lines):
    blocks, current = [], []
    for line in lines:
        if line.strip() == "":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line)
    if current:
        blocks.append(current)
    return blocks


def block_to_dict(block):
    fields = {}
    for line in block:
        parsed = parse_kv(line)
        if parsed:
            fields[parsed[0]] = parsed[1]
    return fields


def parse_info_file(text):
    lines = [line for line in text.splitlines() if not line.lstrip().startswith("#")]

    header_indexes = [i for i, line in enumerate(lines) if SECTION_HEADER.match(line.strip())]
    preamble_lines = lines[: header_indexes[0]] if header_indexes else lines

    preamble = {}
    for line in preamble_lines:
        if not line.strip():
            continue
        parsed = parse_kv(line)
        if parsed:
            preamble[parsed[0]] = parsed[1]

    sections = {}
    for idx, start in enumerate(header_indexes):
        name = SECTION_HEADER.match(lines[start].strip()).group(1).upper()
        end = header_indexes[idx + 1] if idx + 1 < len(header_indexes) else len(lines)
        sections[name] = lines[start + 1 : end]

    return preamble, sections


def build_stats(lines, warnings):
    stats = []
    for block in split_blocks(lines):
        fields = block_to_dict(block)
        label, value = fields.get("LABEL"), fields.get("VALUE")
        if not label or not value:
            warnings.append(f"Skipped a STATS block missing LABEL or VALUE: {fields}")
            continue
        entry = {"label": label, "value": value}
        if fields.get("URL"):
            entry["url"] = fields["URL"]
        stats.append(entry)
    return stats


def build_highlights(lines, warnings):
    highlights = []
    for block in split_blocks(lines):
        fields = block_to_dict(block)
        title = fields.get("TITLE")
        if not title:
            warnings.append(f"Skipped a HIGHLIGHTS block missing TITLE: {fields}")
            continue
        entry = {"title": title}
        if fields.get("DESCRIPTION"):
            entry["description"] = fields["DESCRIPTION"]
        highlights.append(entry)
    return highlights


def build_projects(lines, warnings):
    projects = []
    for block in split_blocks(lines):
        fields = block_to_dict(block)
        title = fields.get("TITLE")
        if not title:
            warnings.append(f"Skipped a PROJECTS block missing TITLE: {fields}")
            continue
        entry = {"title": title}
        if fields.get("DESCRIPTION"):
            entry["description"] = fields["DESCRIPTION"]
        technologies = [t.strip() for t in fields.get("TECHNOLOGIES", "").split(",") if t.strip()]
        if technologies:
            entry["technologies"] = technologies
        if fields.get("LIVE URL"):
            entry["liveUrl"] = fields["LIVE URL"]
        if fields.get("SOURCE URL"):
            entry["sourceUrl"] = fields["SOURCE URL"]
        projects.append(entry)
    return projects


def build_timeline(lines, section_name, warnings):
    items = []
    for block in split_blocks(lines):
        fields = block_to_dict(block)
        title = fields.get("TITLE")
        if not title:
            warnings.append(f"Skipped a {section_name} block missing TITLE: {fields}")
            continue
        entry = {"title": title}
        if fields.get("DATE"):
            entry["date"] = fields["DATE"]
        if fields.get("ORGANIZATION"):
            entry["organization"] = fields["ORGANIZATION"]
        if fields.get("DESCRIPTION"):
            entry["description"] = fields["DESCRIPTION"]
        items.append(entry)
    return items


def build_skills(lines):
    return [line.strip() for line in lines if line.strip()]


def main():
    if not INFO_PATH.exists():
        print(f"Couldn't find {INFO_PATH}")
        sys.exit(1)

    preamble, sections = parse_info_file(INFO_PATH.read_text(encoding="utf-8"))
    warnings = []

    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

    field_map = {
        "NAME": "name",
        "ROLE": "role",
        "LOCATION": "location",
        "SHORT BIO": "bio",
        "ABOUT ME": "about",
        "EMAIL": "email",
        "RESUME URL": "resumeUrl",
    }
    for info_key, profile_key in field_map.items():
        if info_key in preamble:
            profile["profile"][profile_key] = preamble[info_key]

    instagram = preamble.get("INSTAGRAM", "")
    profile["profile"]["socials"] = [{"label": "Instagram", "url": instagram}] if instagram else []

    if "STATS" in sections:
        profile["sections"]["stats"] = build_stats(sections["STATS"], warnings)
    if "SKILLS" in sections:
        profile["sections"]["skills"] = build_skills(sections["SKILLS"])
    if "HIGHLIGHTS" in sections:
        profile["sections"]["highlights"] = build_highlights(sections["HIGHLIGHTS"], warnings)
    if "PROJECTS" in sections:
        profile["sections"]["projects"] = build_projects(sections["PROJECTS"], warnings)
    if "EXPERIENCE" in sections:
        profile["sections"]["experience"] = build_timeline(sections["EXPERIENCE"], "EXPERIENCE", warnings)
    if "EDUCATION" in sections:
        profile["sections"]["education"] = build_timeline(sections["EDUCATION"], "EDUCATION", warnings)

    PROFILE_PATH.write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("Updated content/profile.json from content/my-info.txt.")
    for warning in warnings:
        print(f"Warning: {warning}")
    print("Next: commit and push (or ask Claude to do it) to publish it.")


if __name__ == "__main__":
    main()
