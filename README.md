# Yuki-Anastasia.github.io

Static portfolio website for GitHub Pages.

## Structure

- `index.html` - single-page portfolio shell (home, about, highlights, projects, blog, skills, experience, education).
- `assets/css/styles.css` - responsive visual styling.
- `assets/js/main.js` - renders portfolio content from JSON.
- `assets/img/` - images, portraits, project screenshots, and icons.
- `content/profile.json` - real portfolio content goes here.
- `blog/template.html` - starter template for a local blog post page; copy it per post and link to it from `sections.blog[].url` in `profile.json`.
- `.nojekyll` - keeps GitHub Pages from processing this as a Jekyll site.

## Sections

The page is a single scroll with anchor navigation. Each section is hidden until
its content in `content/profile.json` is non-empty:

- `#home` - hero: name, role, location, short bio, resume/contact buttons.
- `#about` - longer "About Me" copy (`profile.about`).
- `#highlights` - selected achievements (`sections.highlights`).
- `#projects` - project cards with tech tags and live/source links (`sections.projects`).
- `#blog` - post cards with date, excerpt, and a link to the full post (`sections.blog`).
  The `url` field can point to an external post (Medium, dev.to, etc.) or a local
  page you add, e.g. `blog/my-post.html`.
- `#skills` - tag list (`sections.skills`).
- `#experience` / `#education` - timelines (`sections.experience`, `sections.education`).

## Content Needed

Before this site should be published with personal content, fill in:

- Name exactly as it should appear.
- Short professional role/title.
- Location, if you want it public.
- Short hero bio and a longer About Me paragraph.
- Contact links to publish publicly.
- Project titles, descriptions, technologies, and live/source links.
- Blog posts (title, date, excerpt, link), if you plan to write any.
- Work, education, awards, or certificates you want shown.
- Resume file or URL, if you want one linked.
- Profile image and project screenshots.

No placeholder biography or fake project data has been added.

## Local Preview

Because the page loads `content/profile.json`, preview it through a local server:

```powershell
python -m http.server 8000
```

Then open `http://localhost:8000`.

## GitHub Pages

For a user/organization Pages site, the repository should be named:

```text
Yuki-Anastasia.github.io
```

Publish from the default branch root in GitHub Pages settings.

