# AGENTS.md

Context for AI coding agents and human maintainers. The project overview and file map are in `README.md`; this file holds only the rules and gotchas that aren't obvious from the code.

## Project

A static website that runs text2qti (Python) in the browser through PyScript/Pyodide, turning plain-text quizzes into Canvas QTI .zip files. There is no server, build step, framework, or bundler. GitHub Pages serves the repository root of `main` as-is (`.nojekyll`, `CNAME`).

## Run and check

- Serve locally: `python3 -m http.server 8000`, then open `http://localhost:8000/`. Opening files via `file://` does not work, because the pages fetch `.py`, `.toml`, and `.md` files.
- Check the guide examples and compile step: `pip install text2qti==0.8.0 && python3 scripts/check_examples.py`. It must print `OK`.
- After layout or CSS changes, check in a browser at 1280×720 and 1024×640 (no page scrollbar) and at 390 px wide (no horizontal scroll).
- After Python changes, load the page, wait for "Ready.", press **Load example**, then **Download QTI .zip**, and confirm a .zip downloads.

## Rules

- Use plain HTML, CSS, and Python. Do not add a CSS framework, a JS framework, a build step, or npm dependencies. Prefer native elements (`<details>`, `<output>`, `<dialog>`, the `hidden` attribute) over custom widgets.
- Colors come only from the tokens in `css/theme.css`, which are W&L brand colors with their contrast checked. Text must meet WCAG AA contrast, and no text goes below `--text-sm` (0.9375rem). Spring Leaf, Autumn Leaf, Blue Sky, and Footbridge Grey are for decoration only, never text.
- The builder page must fit one desktop screen. The layout depends on `min-height: 0` on flex and grid children in `css/app.css`; keep it.
- Put user-visible text into the DOM with `textContent`, never `innerHTML`. The one exception is `js/render-text.js`, which escapes its input first.
- Keep `run_code_blocks` set to `False` in `py/quizbuild.py`.
- Pin versions. To upgrade PyScript (`index.html`) or text2qti (`pyscript.toml`), read the release notes, rerun every check above, and update the versions in `NOTICE.md`.
- Do not list local files under `[files]` in `pyscript.toml`. It turns off PyScript's package cache. `py/main.py` fetches `py/quizbuild.py` itself instead.
- The guide's `<pre data-example>` blocks double as the sample quiz. Keep them valid text2qti. Wrapped question lines must be indented.

## Legal and attribution

- License: AGPL-3.0-or-later. Every new source file starts with an SPDX header: `SPDX-License-Identifier: AGPL-3.0-or-later` and `Copyright (C) 2026 Nicholas Gardella`. Copy the comment style from a file of the same type.
- Never edit `LICENSE`; it is the verbatim GNU text.
- Keep the attribution "Concept & architecture: Nicholas Gardella" and the text2qti credit in every page footer. AGPL section 7 terms in `NOTICE.md` require it.
- When adding or removing anything loaded at runtime (CDN script, PyPI package), update the third-party section of `NOTICE.md`.

## Change history

`CHANGELOG.md` is the project's audit trail of human direction and AI assistance. For each meaningful change, append a numbered step under "Timeline" that says who asked for what, what was built, and any decision the agent made beyond the literal request. Cite commit hashes only after the commit is final (rebasing changes them).

## Git

- Rebase onto `origin/main` before pushing. The owner sometimes commits directly on GitHub, for example `CNAME`.
- Do not delete `CNAME` or `.nojekyll`.
- Push only when the owner asks.

## Pages that render repository files

`license.html` renders `NOTICE.md` and `LICENSE`, `history.html` renders `CHANGELOG.md`, and `agents.html` renders this file, all through `js/render-text.js`. That renderer supports only headings, paragraphs, flat lists, fenced code, inline code, bold, italics, and links. Do not use tables or nested lists in those Markdown files.
