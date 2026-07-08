const contentPath = "content/profile.json";

const text = (value) => (typeof value === "string" ? value.trim() : "");

const get = (source, path) =>
  path.split(".").reduce((current, key) => (current ? current[key] : undefined), source);

const setText = (element, value, fallback = "") => {
  const next = text(value) || fallback;
  element.textContent = next;
  element.classList.toggle("is-empty", !next);
};

const createLink = (label, href) => {
  if (!text(label) || !text(href)) return null;
  const link = document.createElement("a");
  link.href = href;
  link.textContent = label;
  link.rel = "noopener noreferrer";
  if (/^https?:\/\//i.test(href)) {
    link.target = "_blank";
  }
  return link;
};

const renderEmptyState = (container) => {
  const message = container.dataset.empty;
  if (!message) return;
  const empty = document.createElement("p");
  empty.className = "empty-state";
  empty.textContent = message;
  container.appendChild(empty);
};

const renderActions = (profile) => {
  const resume = document.querySelector("[data-link='profile.resumeUrl']");
  const contact = document.querySelector("[data-email='profile.email']");

  if (resume && text(profile.resumeUrl)) {
    resume.href = profile.resumeUrl;
    resume.hidden = false;
  }

  if (contact && text(profile.email)) {
    contact.href = `mailto:${profile.email}`;
    contact.hidden = false;
  }
};

const renderSocials = (socials) => {
  const container = document.querySelector("[data-social-links]");
  if (!container || !Array.isArray(socials)) return;

  socials.forEach((item) => {
    const link = createLink(item.label, item.url);
    if (link) container.appendChild(link);
  });
};

const renderHighlights = (items, container) => {
  if (items.length === 0) return renderEmptyState(container);

  items.forEach((item) => {
    const card = document.createElement("article");
    card.className = "card";

    const title = document.createElement("h3");
    title.textContent = text(item.title);
    card.appendChild(title);

    if (text(item.description)) {
      const description = document.createElement("p");
      description.textContent = item.description;
      card.appendChild(description);
    }

    container.appendChild(card);
  });
};

const renderProjects = (items, container) => {
  if (items.length === 0) return renderEmptyState(container);

  items.forEach((item) => {
    const card = document.createElement("article");
    card.className = "card";

    const title = document.createElement("h3");
    title.textContent = text(item.title);
    card.appendChild(title);

    if (text(item.description)) {
      const description = document.createElement("p");
      description.textContent = item.description;
      card.appendChild(description);
    }

    if (Array.isArray(item.technologies) && item.technologies.length > 0) {
      const tags = document.createElement("ul");
      tags.className = "tag-list";
      item.technologies.map(text).filter(Boolean).forEach((skill) => {
        const tag = document.createElement("li");
        tag.textContent = skill;
        tags.appendChild(tag);
      });
      card.appendChild(tags);
    }

    const links = document.createElement("div");
    links.className = "card-links";
    [createLink("Live", item.liveUrl), createLink("Source", item.sourceUrl)]
      .filter(Boolean)
      .forEach((link) => links.appendChild(link));
    if (links.children.length > 0) card.appendChild(links);

    container.appendChild(card);
  });
};

const renderBlog = (items, container) => {
  if (items.length === 0) return renderEmptyState(container);

  items.forEach((item) => {
    const card = document.createElement("article");
    card.className = "card";

    if (text(item.date)) {
      const date = document.createElement("p");
      date.className = "blog-date";
      date.textContent = item.date;
      card.appendChild(date);
    }

    const title = document.createElement("h3");
    title.textContent = text(item.title);
    card.appendChild(title);

    if (text(item.excerpt)) {
      const excerpt = document.createElement("p");
      excerpt.textContent = item.excerpt;
      card.appendChild(excerpt);
    }

    const link = createLink("Read", item.url);
    if (link) {
      const links = document.createElement("div");
      links.className = "card-links";
      links.appendChild(link);
      card.appendChild(links);
    }

    container.appendChild(card);
  });
};

const renderSkills = (items, container) => {
  if (items.length === 0) return renderEmptyState(container);

  items.map(text).filter(Boolean).forEach((skill) => {
    const item = document.createElement("li");
    item.textContent = skill;
    container.appendChild(item);
  });
};

const renderTimeline = (container, items) => {
  if (items.length === 0) return renderEmptyState(container);

  items.forEach((item) => {
    const row = document.createElement("article");
    row.className = "timeline-item";

    const date = document.createElement("div");
    date.className = "timeline-date";
    date.textContent = text(item.date);

    const body = document.createElement("div");
    const title = document.createElement("h3");
    title.textContent = text(item.title);
    body.appendChild(title);

    if (text(item.organization)) {
      const organization = document.createElement("p");
      organization.textContent = item.organization;
      body.appendChild(organization);
    }

    if (text(item.description)) {
      const description = document.createElement("p");
      description.textContent = item.description;
      body.appendChild(description);
    }

    row.append(date, body);
    container.appendChild(row);
  });
};

const render = (content) => {
  const profile = content.profile || {};
  const sections = content.sections || {};
  const siteTitle = text(content.site?.title) || text(profile.name) || "Portfolio";
  const description = text(content.site?.description) || text(profile.bio);

  document.documentElement.lang = text(content.site?.language) || "en";
  document.title = siteTitle;

  const metaDescription = document.querySelector("meta[name='description']");
  if (metaDescription) metaDescription.setAttribute("content", description);

  document.documentElement.style.setProperty("--accent", text(content.site?.accentColor) || "#0f766e");

  document.querySelectorAll("[data-bind='site-title'], [data-footer-title]").forEach((element) => {
    setText(element, siteTitle, "Portfolio");
  });

  document.querySelectorAll("[data-field]").forEach((element) => {
    setText(element, get(content, element.dataset.field), element.dataset.fallback || "");
  });

  renderActions(profile);
  renderSocials(profile.socials);

  const highlightsList = document.querySelector("[data-list='highlights']");
  if (highlightsList) renderHighlights(sections.highlights || [], highlightsList);

  const projectsList = document.querySelector("[data-list='projects']");
  if (projectsList) renderProjects(sections.projects || [], projectsList);

  const blogList = document.querySelector("[data-list='blog']");
  if (blogList) renderBlog(sections.blog || [], blogList);

  const skillsList = document.querySelector("[data-list='skills']");
  if (skillsList) renderSkills(sections.skills || [], skillsList);

  const experienceList = document.querySelector("[data-list='experience']");
  if (experienceList) renderTimeline(experienceList, sections.experience || []);

  const educationList = document.querySelector("[data-list='education']");
  if (educationList) renderTimeline(educationList, sections.education || []);

  document.querySelectorAll("[data-section]").forEach((section) => {
    const items = sections[section.dataset.section];
    if (Array.isArray(items) && items.length > 0) section.hidden = false;
  });
};

fetch(contentPath)
  .then((response) => {
    if (!response.ok) throw new Error(`Unable to load ${contentPath}`);
    return response.json();
  })
  .then(render)
  .catch(() => {
    document.documentElement.classList.add("content-unavailable");
  });
