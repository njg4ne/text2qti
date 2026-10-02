# text2qti in the Browser

Write quiz questions as plain text and download a Canvas-ready QTI 1.2 `.zip`, with everything running in your browser.

**Concept & architecture:** [Nicholas Gardella, Ph.D.](https://n.gardella.cc/). The idea is to put Geoffrey M. Poore's [text2qti](https://github.com/gpoore/text2qti) (BSD-3-Clause) in a web page using WebAssembly, so instructors don't have to install anything. The implementation was built with AI coding tools under Nicholas Gardella's direction.

## Files

| Path | Purpose |
|---|---|
| `index.html` | The quiz builder: editor, syntax guide, and download button. |
| `canvas-import.html` | Help page: how to import the `.zip` into a Canvas item bank or quiz. |
| `license.html` | Renders `NOTICE.md` and `LICENSE` as a themed page. |
| `history.html` | Renders `CHANGELOG.md`, the development history and audit trail. |
| `js/render-text.js` | Small, dependency-free renderer that turns those text files into HTML. |
| `LICENSE` | GNU AGPL-3.0, verbatim. |
| `NOTICE.md` | Copyright, intended use, AGPL section 7 terms, third-party licenses, and trademarks. |
| `CHANGELOG.md` | How the app was developed and who directed it. |
| `AGENTS.md` | Rules and checks for AI coding agents and maintainers ([agents.md](https://agents.md/) format). |
| `agents.html` | Student-friendly explainer of agent context files. It also renders `AGENTS.md`. |
| `skills/upgrading-dependencies/SKILL.md` | Step-by-step checklist for upgrading PyScript or text2qti, linked from `AGENTS.md`. |
| `scripts/check_examples.py` | Compiles the guide examples with text2qti and prints `OK` or the error. |
| `css/theme.css` | Shared design tokens (W&L brand colors and type), base styles, and header/footer. |
| `css/app.css` | Builder layout: fits one screen on desktop and stacks on phones. |
| `css/doc.css` | Layout for long-form help pages. |
| `pyscript.toml` | Pins `text2qti==0.8.0`. `py/main.py` fetches `py/quizbuild.py` itself so the package cache stays on. |
| `py/main.py` | Browser glue: button handlers, status messages, and the download. |
| `py/quizbuild.py` | Pure-Python compile step (`build_qti_zip`). It doesn't use browser APIs, so you can test it with plain CPython. |

There's no build step, framework, or JS bundle. The pages use semantic HTML, plain CSS, and one PyScript script tag.

## Running locally

Serve the folder over HTTP. Opening `index.html` as `file://` won't work, because PyScript fetches `pyscript.toml` and the `py/` files:

```sh
python3 -m http.server 8000
# open http://localhost:8000/
```

GitHub Pages (or any static host) works as-is.

## How it works

1. PyScript loads Pyodide (CPython compiled to WebAssembly). micropip then installs text2qti and its pure-Python dependencies (Markdown, bespon) from PyPI.
2. `py/main.py` enables the buttons. Until then they're `disabled` in the HTML.
3. **Download** calls `quizbuild.build_qti_zip(text)`. That calls text2qti's `Quiz` and `QTI` classes directly, and the zip is built in memory. It doesn't use the CLI, temp files, or `~/.text2qti.bespon` config.
4. The bytes are turned into a `Blob`, and a temporary `<a download>` link saves them as `<quiz-title>.zip`.

## Caveats and limitations

- **First load is slow.** The page downloads the Pyodide runtime and packages from CDNs (several MB). Browsers cache them, so later visits are faster.
- **Main-thread execution.** Compiling runs on the UI thread. Normal quizzes compile in milliseconds, but a huge one could briefly freeze the tab. Running it in a PyScript `worker` would fix that.
- **No code execution.** text2qti's executable code blocks (`.run`) are always off. Pyodide can't start subprocesses, and running user-supplied code is out of scope here anyway.
- **No local images.** The browser sandbox has no access to your disk, so image references must be URLs.
- **LaTeX math** renders through Canvas's own `/equation_images/` service after import. It won't render anywhere else.
- **Safari** may auto-unzip downloads. The help page explains how to stop that.
- **Canvas UI drift.** Canvas renames menus from time to time, so check `canvas-import.html` against the current Canvas Instructor Guide now and then.

## Security and privacy

- Quiz text never leaves the browser. There's no server and no analytics.
- Error messages are shown with `textContent`, never `innerHTML`, so quiz text can't inject markup.
- The page trusts pyscript.net, the Pyodide CDN, and PyPI at the pinned versions. Bumping the PyScript or text2qti version means testing again.

## Testing the compile step without a browser

```sh
pip install text2qti==0.8.0
cd py && python -c "import quizbuild; print(quizbuild.build_qti_zip('1. 2+2?\n*a) 4\nb) 5')[0])"
```

## License

Copyright (C) 2026 Nicholas Gardella. Licensed under the **GNU Affero General Public License v3.0 or later** (`AGPL-3.0-or-later`), with additional terms under AGPL section 7. Those terms require keeping the attribution and marking modified versions, and they grant no trademark rights. See [`NOTICE.md`](NOTICE.md), which also lists the third-party licenses (text2qti and its dependencies under BSD-3-Clause, PyScript under Apache-2.0, Pyodide under MPL-2.0). The app is intended for education at public and non-profit institutions.

How the app was built, and by whom, is recorded in [`CHANGELOG.md`](CHANGELOG.md).
