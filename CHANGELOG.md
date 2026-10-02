# Development history

This page is an intellectual audit trail. It records how the app reached its current form, who decided what, and which AI tools were used. It also shows that the project was directed by a person: **Nicholas Gardella** set the goals, made the design calls, and reviewed and accepted every change. The AI tools drafted code under that direction.

Dates are in the author's local time. Commit hashes refer to the [source repository](https://github.com/njg4ne/text2qti).

## People, tools, and roles

- **Nicholas Gardella, Ph.D.** (Assistant Professor of Computer Science, Washington and Lee University). Came up with the idea of running text2qti entirely in the browser so instructors need no install. Set the architecture, wrote the requirements, chose the license, directed the design and accessibility standards, reviewed every result, and decided what was published.
- **Geoffrey M. Poore**. Author of [text2qti](https://github.com/gpoore/text2qti), the quiz parser this app depends on. This app wraps text2qti and does not change it.
- **Google Search AI Mode** (on a Google AI Pro account). Produced the first single-file prototype from Nicholas's prompts.
- **Claude Code** (Anthropic, model Claude Opus 5.5). Rewrote, tested, and documented the app over several directed rounds, described below. Each round started from Nicholas's written instructions.

## Influences

- **Scott Tolinski and the [Syntax.fm](https://syntax.fm/) podcast.** Their platform-first philosophy shaped the rewrite: use native HTML elements and modern CSS before reaching for libraries or frameworks. Nicholas pointed to Tolinski's article [“This component could have been a div”](https://tolin.ski/posts/this-component-could-have-been-a-div) as the standard. That is why the app has no CSS framework, no JS framework, and no build step.
- **Washington and Lee University brand guide.** The source of the color palette (W&L Blue, Liberty Hall Grey, and the secondary colors) and the type choices (Palatino for headings, Arial as the approved sans-serif).
- **Accessibility (WCAG 2.2).** Nicholas required good color contrast and text that isn't too small. Every text color was checked against its background, and nothing reading-sized goes below 15px.
- **Teaching practice in Canvas.** The import guide follows the workflow Nicholas uses: a New Quizzes item bank shared with the course, filled with the ⋯ → Import Content option.

## Timeline

### 0. Starting point: text2qti (upstream)

A command-line Python tool by Geoffrey M. Poore that turns plain-text quizzes into QTI files for Canvas. Instructors have to install Python and run commands in a terminal. The [njg4ne/text2qti](https://github.com/njg4ne/text2qti) repository began as a GitHub fork of it, and its history up to commit `80dac05` is upstream's work.

### 1. Prototype with Google Search AI Mode (2026-10-02)

Nicholas asked Google Search AI Mode for a web page that runs text2qti in the browser. The result was one `index.html` file that:

- loaded PyScript 2024.1.1 and the Tailwind CSS CDN;
- installed `text2qti` and `Markdown` in the browser;
- called text2qti's *command-line* entry point by faking `sys.argv` and writing temporary files;
- showed a syntax guide (multiple choice, multiple answers, numerical, essay, file upload) and a credits box that described the AI's role as "AI Technical Collaborator (Developed by Google)".

The idea, the requirements, and the decision to build it in the browser came from Nicholas. The first draft of the code came from Google's tool.

### 2. Publish and correct attribution (2026-10-02, commit `8654090`)

Directed by Nicholas, carried out with Claude Code:

- Cloned the fork and replaced the contents of `main` with the prototype. This was a normal commit, so upstream history stays intact.
- Rewrote the credits so Nicholas is named as the architect of the idea, with text2qti credited as the parser.
- Added the missing **non-numeric short-answer** (fill-in-the-blank) example to the guide, after Nicholas pointed out the gap.
- Checked that every guide example compiles with the real text2qti package.

### 3. Redesign, accessibility, and Canvas guide (2026-10-02, commit `227f9e5`)

Nicholas's instructions: use CSS best practices in the spirit of Tolinski's article; use W&L colors; make the app accessible with good contrast and readable text sizes; get rid of the page scrollbar at normal zoom; write a simple help page on importing the .zip into Canvas (enable New Quizzes, item bank, share with the course, ⋯ → Import Content), linked from the app; split the code into readable files with comments on caveats, performance, security, and possible bugs.

What was built in response:

- Removed Tailwind and rewrote the page as semantic HTML with plain CSS: `<main>`, `<aside>`, `<output role="status">`, the `hidden` attribute, and a skip link.
- Added shared design tokens in `css/theme.css` built on the W&L palette, with a contrast note for each color. The light brand colors are used only as decoration.
- Fixed the scrollbar with `box-sizing: border-box`, a full-height flex column, and a grid with `min-height: 0`. Tested with no overflow at 1024×640, 1280×720, 1366×768, and 1440×900. Phones stack the layout and scroll normally.
- Added `canvas-import.html` and linked it from the builder and from the message shown after a download.
- Split the Python into `py/quizbuild.py` (pure compile step, testable without a browser) and `py/main.py` (browser glue). It now calls text2qti's library classes directly and builds the zip in memory.
- Robustness fixes: buttons stay disabled until Python has loaded, the download link isn't released too early, error text is shown with `textContent`, and package versions are pinned.
- Added a "Load example" button that reads the guide's own examples, so the two can never drift apart.
- Placed the editor first in the HTML for screen readers and phones. On wide screens CSS still shows it in the right-hand column.
- Verified end to end in headless Chrome: the page loads, the example compiles, the .zip downloads, and syntax errors are reported with line numbers.

### 4. Licensing, notices, and this audit trail (2026-10-02)

Nicholas's instructions: choose the most suitable license that stops others from profiting from the code without open-sourcing their changes; list all other licenses and intellectual property as compliantly as possible; state that the intended use is education at public and non-profit institutions; show the license as a readable page in the app's style; add this history page.

What was built in response:

- Licensed the project under **GNU AGPL-3.0-or-later**. It is the standard open-source license that requires source code to be shared even when a modified version is only offered as a website. Section 7 additional terms require keeping Nicholas's attribution, marking modified versions, and grant no trademark rights.
- Wrote `NOTICE.md`, covering the intended-use statement, the third-party components and their licenses (text2qti, Python-Markdown, BespON, PyScript, Pyodide/CPython), trademarks (W&L, Instructure/Canvas, 1EdTech/QTI, and others), and a note on AI-assisted development.
- Added `license.html` and `history.html`. Both render `NOTICE.md`, `LICENSE`, and this file directly from the repository text, so the website and GitHub always show the same words.
- Added a "Source code" link and license links to every page footer, as AGPL section 13 expects for software used over a network.

## How oversight worked

- Every change started from a written instruction by Nicholas. The AI tools did not choose the project's goals, its license, or what was published.
- AI output was checked before acceptance by running the real text2qti package on the examples, measuring layouts in a real browser, and looking at screenshots.
- AI-introduced decisions that went beyond the literal request are listed above so they can be reviewed. Examples are calling text2qti's library classes instead of its command line, and reordering the editor for accessibility.
- Pushing to the public repository happened only when Nicholas asked for it.
