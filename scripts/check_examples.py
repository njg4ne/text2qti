# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Nicholas Gardella
"""
Compile every <pre data-example> block in index.html with text2qti, joined
the same way the "Load example" button joins them. Exit code 0 = all good.

    pip install text2qti==0.8.0
    python3 scripts/check_examples.py

Run this after editing the syntax guide or py/quizbuild.py.
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "py"))

from quizbuild import Text2qtiError, build_qti_zip  # noqa: E402

page = (ROOT / "index.html").read_text(encoding="utf-8")
page = re.sub(r"<!--.*?-->", "", page, flags=re.S)  # comments mention the tag too
blocks = [html.unescape(b) for b in re.findall(r"<pre data-example>(.*?)</pre>", page, re.S)]
if not blocks:
    sys.exit("FAIL: no <pre data-example> blocks found in index.html")

try:
    name, data = build_qti_zip("\n\n".join(blocks) + "\n")
except Text2qtiError as err:
    sys.exit(f"FAIL: guide examples do not compile:\n{err}")

print(f"OK: {len(blocks)} example blocks compiled to {name} ({len(data)} bytes)")
