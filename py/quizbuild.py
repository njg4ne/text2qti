# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Nicholas Gardella
"""
quizbuild.py — pure-Python quiz compilation (no browser APIs).

Kept separate from main.py so it can be unit-tested with plain CPython:

    pip install text2qti==0.8.0
    python -c "import quizbuild; print(quizbuild.build_qti_zip(open('q.txt').read())[0])"

We call text2qti's library classes directly instead of its command-line
entry point (text2qti.cmdline.main). That avoids:
  * argv / os.chdir / file-system round trips (the zip is built in memory);
  * Config.load(), which reads/writes ~/.text2qti.bespon — meaningless in a
    browser sandbox;
  * sys.exit() on argparse errors, which would surface as a confusing
    SystemExit in the page.
"""

import re

from text2qti.config import Config
from text2qti.err import Text2qtiError
from text2qti.qti import QTI
from text2qti.quiz import Quiz

__all__ = ["build_qti_zip", "Text2qtiError"]

# Used only in error messages ("In "quiz.txt" on line 3: ...").
SOURCE_NAME = "quiz.txt"


def _config() -> Config:
    """Build a fresh config for every compile (no state leaks between runs)."""
    config = Config()
    # SECURITY: never execute code blocks from user text. This is already
    # text2qti's default; set explicitly so the intent is documented here.
    # (Pyodide has no subprocess support anyway, so it could not work.)
    config["run_code_blocks"] = False
    # LaTeX math is rendered as <img src="/equation_images/..."> which Canvas
    # serves itself, so the default relative URL is correct after import.
    return config


def _slugify(title: str) -> str:
    """'Week 3: Sorting!' -> 'week-3-sorting' (safe as a download filename)."""
    slug = re.sub(r"[^A-Za-z0-9]+", "-", title).strip("-").lower()
    return slug[:60] or "quiz"


def build_qti_zip(text: str) -> tuple[str, bytes]:
    """
    Compile text2qti markup into a QTI 1.2 zip.

    Returns (suggested_filename, zip_bytes).
    Raises Text2qtiError for problems in the quiz text (with line numbers)
    and ValueError for empty input.
    """
    if not text.strip():
        raise ValueError("The quiz text is empty. Type some questions or press “Load example”.")

    quiz = Quiz(text, config=_config(), source_name=SOURCE_NAME)
    zip_bytes = QTI(quiz).zip_bytes()
    return f"{_slugify(quiz.title_raw or '')}.zip", zip_bytes
