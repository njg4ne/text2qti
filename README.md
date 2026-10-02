# text2qti in the Browser

Write quiz questions as plain text and download a Canvas-ready QTI 1.2 `.zip`, with everything running in your browser.

**Concept & architecture:** [Nicholas Gardella, Ph.D.](https://n.gardella.cc/). The idea is to put Geoffrey M. Poore's [text2qti](https://github.com/gpoore/text2qti) (BSD-3-Clause) in a web page using WebAssembly, so instructors don't have to install anything. The implementation was built with AI coding tools under Nicholas Gardella's direction.

## Files

| Path | Purpose |
|---|---|
| `index.html` | The quiz builder: editor, syntax guide, and download button. |
| `canvas-import.html` | Help page: how to import the `.zip` into a Canvas item bank or quiz. |
| `css/theme.css` | Shared design tokens (W&L brand colors and type), base styles, and header/footer. |
| `css/app.css` | Builder layout: fits one screen on desktop and stacks on phones. |
| `css/doc.css` | Layout for long-form help pages. |
| `pyscript.toml` | Pins `text2qti==0.8.0` and copies `py/quizbuild.py` into Pyodide. |
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
