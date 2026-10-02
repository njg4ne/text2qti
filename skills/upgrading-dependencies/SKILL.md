---
name: upgrading-dependencies
description: Upgrades the pinned PyScript (and its bundled Pyodide) or text2qti version for this static site, then verifies the build and updates the license notices and changelog. Use when asked to upgrade, bump, or update PyScript, Pyodide, or text2qti, or when a pinned version looks outdated.
---

# Upgrading dependencies

Upgrades are the riskiest change in this repo: everything loads from CDNs at runtime, so a broken version only shows up in a browser. Upgrade one dependency at a time.

Copy this checklist and tick it off:

```
- [ ] 1. Find the current pins
- [ ] 2. Read the release notes for breaking changes
- [ ] 3. Update every pin
- [ ] 4. Run the compile check
- [ ] 5. Test in a browser
- [ ] 6. Update NOTICE.md, the changelog, and the docs
```

## 1. Find the current pins

```bash
grep -rn -E "pyscript.net/releases/|text2qti==|PyScript [0-9]|Pyodide [0-9]|text2qti [0-9]" . --exclude-dir=.git --exclude=CHANGELOG.md
```

- PyScript: the `core.js` URL in `index.html`. The Pyodide version comes with PyScript and is not pinned separately.
- text2qti: `packages` in `pyscript.toml`, plus the `pip install` lines in `README.md`, `AGENTS.md`, `py/quizbuild.py`, and `scripts/check_examples.py`.

## 2. Read the release notes

- PyScript: https://github.com/pyscript/pyscript/releases. Read every release between the current pin and the target, not just the latest.
- text2qti: https://github.com/gpoore/text2qti/blob/main/CHANGELOG.md and https://pypi.org/project/text2qti/

Look for changes to what this repo relies on:

- PyScript config handling (`packages`, `[files]`). Since 2026.7, `[files]` entries for local files turn off the package cache.
- The `pyscript` module API used in `py/main.py`: `document`, `window`, `when`, `fetch`, and `pyscript.ffi.to_js`, plus top-level `await`.
- The Python version in the new Pyodide, compared with text2qti's `requires-python`.
- The text2qti library API used in `py/quizbuild.py`: `Quiz(text, config=, source_name=)`, `QTI(quiz).zip_bytes()`, `quiz.title_raw`, `Config`, `Text2qtiError`, and the `run_code_blocks` key.

If something breaks, adapt the code. Don't skip the upgrade or pin an in-between version silently.

## 3. Update every pin

Change every hit from step 1, then rerun the grep. No old version should remain outside `CHANGELOG.md`.

## 4. Run the compile check

```bash
python3 -m venv /tmp/t2q && /tmp/t2q/bin/pip install -q "text2qti==NEW" && /tmp/t2q/bin/python scripts/check_examples.py
```

It must print `OK`. If it fails, fix the code and run it again before continuing.

## 5. Test in a browser

Serve with `python3 -m http.server 8000`, open `http://localhost:8000/`, then:

- wait for the status to read "Ready." (the first load downloads the runtime);
- check the console for errors (a missing favicon 404 is fine);
- press **Load example**, then **Download QTI .zip**, and confirm the .zip opens and contains `imsmanifest.xml`;
- type `1. hi` and `zz` on two lines, press Download, and confirm the error message shows a line number;
- to find the Pyodide version for `NOTICE.md`, look in the network panel for `cdn.jsdelivr.net/pyodide/v<version>/`.

If a step fails and you can't fix it, revert all the pins and report what broke.

## 6. Update the docs

- `NOTICE.md`: the version in each affected "Third-party components" heading. If a new runtime dependency appears, add an entry with its license.
- `CHANGELOG.md`: add a Timeline step saying who asked, the old and new versions, any code changes, and how the result was verified.
- `README.md` and `AGENTS.md`: change them only if the upgrade changed how something works.
