// SPDX-License-Identifier: AGPL-3.0-or-later
// Copyright (C) 2026 Nicholas Gardella
/*
 * render-text.js — show the repository's own text files (LICENSE, NOTICE.md,
 * CHANGELOG.md) as themed, readable HTML, so the website and GitHub always
 * display the same words with no copy to keep in sync.
 *
 * Usage: any element with  data-render-src="FILE"  data-render-format="markdown|license"
 * is fetched and its contents replaced with rendered HTML. Put a fallback
 * link to the raw file inside the element; it stays visible if fetching fails.
 *
 * Why not a Markdown library? The inputs are a few files we write ourselves,
 * so a small, dependency-free renderer for the subset we use is enough
 * (headings, paragraphs, flat lists, fenced code, `code`, **bold**, *em*,
 * [links](url)). Anything else shows up as plain text, never as markup.
 *
 * SECURITY: every line is HTML-escaped *before* inline formatting runs, and
 * link targets are restricted to http(s), mailto, relative paths and #anchors,
 * so even a malicious file could not inject script.
 *
 * Caveat: needs to be served over http(s); fetch() of local files is blocked
 * on file:// pages.
 */

// Repository files that have their own page on the website. Links to them
// inside rendered Markdown point at the themed page instead of raw text.
const PAGE_FOR_FILE = {
  "CHANGELOG.md": "history.html",
  "NOTICE.md": "license.html",
  "LICENSE": "license.html#license-text",
};

const escapeHtml = (s) =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

const slugify = (s) =>
  s.toLowerCase().replace(/<[^>]+>/g, "").replace(/&[a-z]+;/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

function safeHref(url) {
  if (url in PAGE_FOR_FILE) return PAGE_FOR_FILE[url];
  // Allow absolute http(s)/mailto, plain relative paths, and #anchors only.
  return /^(https?:|mailto:|#|[\w./-]+$)/i.test(url) ? url : "#";
}

/** Inline Markdown on ONE escaped line of text. Code spans are protected. */
function inline(escaped) {
  return escaped
    .split(/(`[^`]+`)/)
    .map((part) => {
      if (/^`[^`]+`$/.test(part)) return `<code>${part.slice(1, -1)}</code>`;
      return part
        .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, text, url) => `<a href="${safeHref(url)}">${text}</a>`)
        .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
        .replace(/(^|[\s(])\*([^*\s][^*]*)\*/g, "$1<em>$2</em>");
    })
    .join("");
}

/** Render our Markdown subset to an HTML string. */
export function renderMarkdown(source) {
  const lines = source.replace(/\r\n?/g, "\n").split("\n");
  const out = [];
  let para = [];   // lines of the current paragraph
  let list = null; // { tag: "ul"|"ol", items: [string] }

  const flushPara = () => {
    if (para.length) out.push(`<p>${para.map((l) => inline(escapeHtml(l))).join("<br>")}</p>`);
    para = [];
  };
  const flushList = () => {
    if (list) out.push(`<${list.tag}>${list.items.map((i) => `<li>${inline(escapeHtml(i))}</li>`).join("")}</${list.tag}>`);
    list = null;
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Fenced code block: copy verbatim (escaped) until the closing fence.
    if (line.startsWith("```")) {
      flushPara(); flushList();
      const code = [];
      while (++i < lines.length && !lines[i].startsWith("```")) code.push(lines[i]);
      out.push(`<pre>${escapeHtml(code.join("\n"))}</pre>`);
      continue;
    }

    const heading = line.match(/^(#{1,4})\s+(.*)$/);
    if (heading) {
      flushPara(); flushList();
      const level = heading[1].length;
      const html = inline(escapeHtml(heading[2]));
      out.push(`<h${level} id="${slugify(html)}">${html}</h${level}>`);
      continue;
    }

    const bullet = line.match(/^- (.*)$/);
    const numbered = line.match(/^\d+\. (.*)$/);
    if (bullet || numbered) {
      flushPara();
      const tag = bullet ? "ul" : "ol";
      if (!list || list.tag !== tag) { flushList(); list = { tag, items: [] }; }
      list.items.push((bullet || numbered)[1]);
      continue;
    }

    // Indented continuation of the previous list item.
    if (list && /^\s{2,}\S/.test(line)) {
      list.items[list.items.length - 1] += " " + line.trim();
      continue;
    }

    if (line.trim() === "") { flushPara(); flushList(); continue; }

    flushList();
    para.push(line);
  }
  flushPara(); flushList();
  return out.join("\n");
}

/**
 * Render a GNU-style plain-text license (blocks separated by blank lines).
 *   - blocks indented 8+ spaces (centered titles)  -> <h3>
 *   - "  N. Title."                                  -> <h4 id="section-N">
 * (The host page supplies the <h2> above the license, so levels start at 3.)
 *   - blocks indented 4+ spaces                      -> indented paragraph
 *     (line breaks kept unless it is an "a) ..." clause)
 *   - everything else                                -> reflowed <p>
 * Also turns <https://...> into links.
 */
export function renderLicense(source) {
  const linkify = (html) => html.replace(/&lt;(https?:\/\/[^\s&]+)&gt;/g, '&lt;<a href="$1">$1</a>&gt;');
  const blocks = source.replace(/\r\n?/g, "\n").split(/\n\s*\n/);
  const out = [];
  const toc = [];

  for (const block of blocks) {
    const lines = block.split("\n").filter((l) => l.trim() !== "");
    if (!lines.length) continue;
    const indents = lines.map((l) => l.match(/^\s*/)[0].length);
    const minIndent = Math.min(...indents);
    const text = escapeHtml(lines.map((l) => l.trim()).join(" "));

    const section = lines.length === 1 && lines[0].match(/^\s{0,3}(\d+)\.\s+(.+)$/);
    if (section) {
      const id = `section-${section[1]}`;
      toc.push(`<li><a href="#${id}">${escapeHtml(lines[0].trim())}</a></li>`);
      out.push(`<h4 id="${id}">${escapeHtml(lines[0].trim())}</h4>`);
    } else if (minIndent >= 8) {
      out.push(`<h3>${lines.map((l) => escapeHtml(l.trim())).join("<br>")}</h3>`);
    } else if (minIndent >= 4) {
      const clause = /^[a-z]\)/.test(lines[0].trim());
      const body = clause ? text : lines.map((l) => escapeHtml(l.trim())).join("<br>");
      out.push(`<p class="indented">${linkify(body)}</p>`);
    } else {
      out.push(`<p>${linkify(text)}</p>`);
    }
  }

  const nav = toc.length
    ? `<details class="license-toc"><summary>Jump to a section</summary><ol>${toc.join("")}</ol></details>`
    : "";
  return nav + out.join("\n");
}

const RENDERERS = { markdown: renderMarkdown, license: renderLicense };

async function renderInto(el) {
  const src = el.dataset.renderSrc;
  const render = RENDERERS[el.dataset.renderFormat] ?? renderMarkdown;
  try {
    const res = await fetch(src);
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    el.innerHTML = render(await res.text()); // safe: renderers escape all input
    el.setAttribute("aria-busy", "false");
    // Honor #fragment links into content that did not exist at page load.
    if (location.hash) document.getElementById(location.hash.slice(1))?.scrollIntoView();
  } catch (err) {
    el.setAttribute("aria-busy", "false");
    console.error(`Could not load ${src}:`, err); // fallback link stays visible
  }
}

document.querySelectorAll("[data-render-src]").forEach(renderInto);
