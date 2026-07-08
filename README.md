# Yuki-Anastasia.github.io

Static portfolio website for GitHub Pages.

## Structure

A dark, portal-driven layout inspired by teamlab.art: the homepage is a landing
screen with a name/role/bio and three large "portal" tiles that link out to
dedicated pages, instead of one long scrolling page.

- `index.html` - landing page: hero (name, role, location, bio) + portal grid
  linking to About, Projects, and Blog.
- `about.html` - About Me copy, highlights, skills, experience, education.
- `projects.html` - project cards with tech tags and live/source links.
- `blog.html` - post cards with date, excerpt, and a link to the full post.
- `assets/css/styles.css` - shared dark theme, portal grid, and page styling.
- `assets/js/main.js` - renders whichever section exists on the current page
  from JSON (each page only renders the elements present in its own HTML).
- `assets/img/` - images, portraits, project screenshots, and icons.
- `content/profile.json` - real portfolio content goes here.
- `blog/template.html` - starter template for a local blog post page; copy it per post and link to it from `sections.blog[].url` in `profile.json`.
- `.nojekyll` - keeps GitHub Pages from processing this as a Jekyll site.

## Pages & sections

Content is hidden until it's filled in in `content/profile.json`:

- **Home** (`index.html`) - hero always shows; the About/Projects/Blog portal
  tiles are always visible since they're the primary navigation.
- **About** (`about.html`) - `profile.about` always shows (even as a short
  placeholder); Highlights, Skills, Experience, and Education each stay
  hidden until their array in `sections` has at least one item.
- **Projects** (`projects.html`) - renders `sections.projects` as cards; shows
  a "coming soon" message in the grid when the array is empty.
- **Blog** (`blog.html`) - renders `sections.blog` as cards; shows a "coming
  soon" message when empty. The `url` field on each post can point to an
  external post (Medium, dev.to, etc.) or a local page you add, e.g.
  `blog/my-post.html`.

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

