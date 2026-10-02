# License and notices

text2qti in the Browser
Copyright (C) 2026 Nicholas Gardella

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program (the `LICENSE` file). If not, see [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/).

SPDX-License-Identifier: `AGPL-3.0-or-later`

Source code: [https://github.com/njg4ne/text2qti](https://github.com/njg4ne/text2qti)

## What this license means in practice

This is a plain-language summary, not legal advice. The `LICENSE` file is what governs.

- **You may** use, study, copy, modify, and share this app, including for free at any school.
- **If you share a modified version** or **run one as a website other people use**, you must make your complete source code available to its users under this same license. The website case is covered by section 13 of the AGPL.
- **You may charge money**, but you cannot keep your changes closed. Every recipient and every website user gets the same freedoms you did.
- **There is no warranty.** Check every quiz in Canvas before students see it.

## Intended use

This app was created for **teaching and learning at public and non-profit educational institutions**. That is a statement of the author's intent and a request to users. It is **not** an extra restriction on the license, because the AGPL does not allow added restrictions on who may use the software.

If the AGPL's terms do not fit what you want to do, contact the copyright holder at [n.gardella.cc](https://n.gardella.cc/) to discuss other arrangements.

## Additional terms under AGPL section 7

As permitted by section 7(b), 7(c) and 7(e) of the GNU Affero General Public License, version 3, the following additional terms apply to this work:

1. **Attribution (7(b)).** Modified versions must keep, in their user interface and documentation, the author attribution "Concept & architecture: Nicholas Gardella" (or reasonably equivalent wording) together with a link to this project's source, and must keep the credit to text2qti by Geoffrey M. Poore.
2. **Marking modified versions (7(c)).** Modified versions must be clearly marked as different from the original version, for example by changing the page title or adding a "modified by" notice. They must not be presented as the original author's version.
3. **No trademark rights (7(e)).** This license grants no rights to use the names, logos, or trademarks of Washington and Lee University, of Nicholas Gardella, or of any other party mentioned here, except as needed to describe where the work came from.

## Third-party components

This repository contains only original files (HTML, CSS, Python, and documentation). The components below are **not stored in this repository**. Each visitor's browser downloads them from their original publishers when the page loads. They are listed here for credit, to keep their notices intact, and for anyone who repackages the app with these components bundled in.

### text2qti 0.8.0: the quiz parser that does the real work

- Author: Geoffrey M. Poore
- License: BSD-3-Clause
- Source: [https://github.com/gpoore/text2qti](https://github.com/gpoore/text2qti)
- Loaded from: PyPI (pypi.org / files.pythonhosted.org)

This project's Git repository began as a GitHub fork of text2qti. Earlier commits in its history contain text2qti's source code and its original `LICENSE.txt`, which remain under the license below.

```
BSD 3-Clause License

Copyright (c) 2020-2026, Geoffrey M. Poore
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### Python-Markdown: a dependency of text2qti

- License: BSD-3-Clause
- Source: [https://github.com/Python-Markdown/markdown](https://github.com/Python-Markdown/markdown)
- Loaded from: PyPI (latest version that text2qti accepts)

```
Copyright 2007, 2008 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

Distributed under the BSD 3-Clause License, with the same conditions and
disclaimer as reproduced for text2qti above.
```

### BespON: a dependency of text2qti

- License: BSD-3-Clause
- Source: [https://github.com/gpoore/bespon_py](https://github.com/gpoore/bespon_py)
- Loaded from: PyPI

```
Copyright 2016-2017 Geoffrey M. Poore

Distributed under the BSD 3-Clause License, with the same conditions and
disclaimer as reproduced for text2qti above.
```

### PyScript 2024.1.1: runs Python in the page

- License: Apache License 2.0
- Source: [https://github.com/pyscript/pyscript](https://github.com/pyscript/pyscript)
- Loaded from: pyscript.net
- License text: [https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)

### Pyodide 0.24.1: CPython compiled to WebAssembly

- License: Mozilla Public License 2.0. Pyodide bundles CPython, which is under the Python Software Foundation License, and other packages under their own licenses.
- Source: [https://github.com/pyodide/pyodide](https://github.com/pyodide/pyodide)
- Loaded from: cdn.jsdelivr.net
- License texts: [https://www.mozilla.org/en-US/MPL/2.0/](https://www.mozilla.org/en-US/MPL/2.0/) and [https://docs.python.org/3/license.html](https://docs.python.org/3/license.html)

All of these licenses are compatible with distributing this app under the AGPL-3.0-or-later.

## Trademarks and other names

- **Washington and Lee University**, "W&L", and the W&L brand colors belong to Washington and Lee University. The color palette and typefaces follow the [W&L brand guide](https://my.wlu.edu/communications-and-public-affairs/washington-and-lee-university-brand-guide/color-and-typography). This is a faculty-created teaching tool. It is not an official university product, and W&L does not endorse it unless the university says so.
- **Canvas** and **Instructure** are trademarks of Instructure, Inc. This project is not affiliated with or endorsed by Instructure.
- **QTI** (Question and Test Interoperability) is a specification of 1EdTech Consortium (formerly IMS Global Learning Consortium).
- **Safari** is a trademark of Apple Inc. **Google** is a trademark of Google LLC. **Claude** and **Claude Code** are trademarks of Anthropic, PBC.
- Fonts (Palatino, Arial, and system monospace fonts) are not distributed with this project. The browser uses whatever is installed on the reader's computer.

## AI-assisted development

Parts of this code were drafted with AI tools under the direction and review of Nicholas Gardella. The [development history](CHANGELOG.md) records what was produced by whom. The copyright claimed above covers the human-authored creative work: the concept, architecture, requirements, design decisions, selection and arrangement, and edits. Any purely machine-generated material that is not eligible for copyright is still provided under the same terms, to the extent anyone holds rights in it.
