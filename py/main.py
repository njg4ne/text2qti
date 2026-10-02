# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Nicholas Gardella
"""
main.py — browser glue for index.html (runs inside PyScript/Pyodide).

Flow:
  1. PyScript downloads Pyodide + text2qti (see pyscript.toml), then runs
     this file. Until then both buttons are `disabled` in the HTML, so the
     user can't click something that has no handler yet.
  2. We fetch py/quizbuild.py, import it, attach the click handlers
     (via @when) and flip the status to "ready".
  3. On "Download", quizbuild.build_qti_zip() returns bytes, which we wrap
     in a Blob and hand to the browser as a download.

Caveats / known limitations:
  * Pyodide runs on the main thread, so the page is unresponsive while a
    quiz compiles. That is milliseconds for normal quizzes; a quiz with
    thousands of questions could freeze the tab briefly. Moving this into
    a Web Worker (PyScript `worker` attribute) would fix it, at the cost of
    more plumbing.
  * Because compilation is synchronous, status text set right before it
    won't paint until it finishes — so we don't show a "compiling…" message.
  * Safari can auto-open "safe" downloads and unzip them; the help page
    tells users to upload the .zip itself, not the extracted folder.
"""

import sys

from pyscript import document, fetch, when, window
from pyscript.ffi import to_js

# Load our helper module. PyScript's [files] config could copy it in for us,
# but since PyScript 2026.7 listing local files in the config turns off the
# browser's package cache, which would make every visit re-download text2qti.
# Fetching it here keeps that cache. (Top-level await is allowed in PyScript.)
_source = await (await fetch("py/quizbuild.py")).text()  # noqa: F704
with open("quizbuild.py", "w", encoding="utf-8") as _f:
    _f.write(_source)
sys.path.insert(0, ".")

from quizbuild import Text2qtiError, build_qti_zip  # noqa: E402

quiz_input = document.getElementById("quiz-input")
generate_btn = document.getElementById("generate-btn")
example_btn = document.getElementById("example-btn")
status = document.getElementById("status")
error_output = document.getElementById("error-output")

# Object URL from the previous download. We revoke it on the *next*
# download rather than immediately after link.click(): some browsers start
# the download asynchronously, and revoking too early can cancel it.
_last_url = None


def set_status(message: str, state: str) -> None:
    """state is one of: loading | ready | success | error (styled in app.css)."""
    status.textContent = message
    status.dataset.state = state


def show_error(message: str) -> None:
    # textContent (never innerHTML): the message can echo user input, so
    # this keeps it from being interpreted as markup.
    error_output.textContent = message
    error_output.hidden = False


def clear_error() -> None:
    error_output.textContent = ""
    error_output.hidden = True


def trigger_download(filename: str, data: bytes) -> None:
    global _last_url
    if _last_url is not None:
        window.URL.revokeObjectURL(_last_url)

    # pyscript.ffi.to_js turns the dict into a plain JS object.
    blob = window.Blob.new([window.Uint8Array.new(data)], to_js({"type": "application/zip"}))
    _last_url = window.URL.createObjectURL(blob)

    link = document.createElement("a")
    link.href = _last_url
    link.download = filename
    link.click()  # a detached <a> works in all current browsers


# @when attaches the handler and keeps its JS proxy alive for us (older
# PyScript needed manual create_proxy() bookkeeping).
@when("click", "#generate-btn")
def on_generate(_event) -> None:
    clear_error()
    try:
        filename, data = build_qti_zip(quiz_input.value)
    except (Text2qtiError, ValueError) as err:
        # Expected problems in the quiz text: show text2qti's message,
        # which includes the line number.
        set_status("Could not build the quiz — see the message below.", "error")
        show_error(str(err))
        return
    except Exception as err:  # noqa: BLE001 — surface anything unexpected
        set_status("Something went wrong inside text2qti.", "error")
        show_error(f"{type(err).__name__}: {err}")
        return

    trigger_download(filename, data)
    set_status(f"Downloaded {filename}. Next: import it into Canvas (link below).", "success")


@when("click", "#example-btn")
def on_load_example(_event) -> None:
    # The guide's <pre data-example> blocks double as the sample quiz.
    blocks = document.querySelectorAll("pre[data-example]")
    quiz_input.value = "\n\n".join(block.textContent for block in blocks) + "\n"
    quiz_input.focus()
    clear_error()


# Handlers are attached; now let people use the buttons.
generate_btn.disabled = False
example_btn.disabled = False
set_status("Ready.", "ready")
