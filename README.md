# Dynamic Evolution reveal.js slides

This repository is set up as a Quarto + reveal.js presentation, with content organized using the same file-structure idea as [`tidy-revealjs`](https://github.com/julie-ng/tidy-revealjs#slides-via-file-structure).

## Slide structure

Slides live in `/slides` and are read in alphabetical order.

- Numbered files control the horizontal slide order.
- Numbered folders create a reveal.js vertical stack.
- The first file in a folder becomes the stack's top slide.
- Remaining files in that folder become vertical follow-up slides.

Example:

```text
slides/
├── 10-overview.qmd
├── 20-workflow.qmd
└── 30-deep-dive/
    ├── 10-model.qmd
    └── 20-follow-up.qmd
```

Each slide fragment should start with a Markdown heading. The build script normalizes heading levels so that top-level files become horizontal slides and subfolder files become vertical slides.

## Getting started

Install the project dependencies with Pixi:

```bash
pixi install
```

Build the assembled slide deck:

```bash
pixi run build-slides
```

Render the reveal.js presentation:

```bash
pixi run render
```

Preview locally:

```bash
pixi run preview
```

The assembled presentation source is written to `/_generated/slides.qmd`, and the rendered site is written to `/_site/`.
