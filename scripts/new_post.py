"""Start a new Blog post.

Run it (double-click New Blog Post.bat, or `python scripts/new_post.py`),
answer the prompts, then open the new file it creates in blog/ and write
the rest of the post. Commit + push when you're ready to publish.
"""

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"
TEMPLATE_PATH = BLOG_DIR / "template.html"
PROFILE_PATH = ROOT / "content" / "profile.json"


def slugify(value):
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return value or "post"


def unique_path(directory, slug):
    candidate = directory / f"{slug}.html"
    counter = 2
    while candidate.exists():
        candidate = directory / f"{slug}-{counter}.html"
        counter += 1
    return candidate


def main():
    title = input("Post title: ").strip()
    if not title:
        print("A title is required.")
        return

    excerpt = input("One or two sentences for the blog list (optional): ").strip()

    today_date = date.today()
    today = f"{today_date:%B} {today_date.day}, {today_date:%Y}"

    slug = slugify(title)
    post_path = unique_path(BLOG_DIR, slug)

    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    html = html.replace("<title>Post Title</title>", f"<title>{title}</title>")
    html = html.replace("<h1>Post Title</h1>", f"<h1>{title}</h1>")
    html = html.replace("<p class=\"blog-date\">Month DD, YYYY</p>", f'<p class="blog-date">{today}</p>')
    if excerpt:
        html = html.replace("<p>Write the post content here.</p>", f"<p>{excerpt}</p>")
    post_path.write_text(html, encoding="utf-8")

    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    entry = {
        "date": today,
        "title": title,
        "excerpt": excerpt,
        "url": post_path.relative_to(ROOT).as_posix(),
    }
    profile["sections"]["blog"].insert(0, entry)
    PROFILE_PATH.write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nCreated {post_path.relative_to(ROOT)}")
    print("Next: open that file and write the rest of the post (edit the <article> paragraphs),")
    print("then commit and push (or ask Claude to do it) to publish it.")


if __name__ == "__main__":
    main()
