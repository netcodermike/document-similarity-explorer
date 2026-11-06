# Document Similarity Explorer

Compare local text documents with TF-IDF cosine similarity and threshold-based connected clusters.

[![Build and verify](https://github.com/netcodermike/document-similarity-explorer/actions/workflows/verify.yml/badge.svg)](https://github.com/netcodermike/document-similarity-explorer/actions/workflows/verify.yml)

**Language:** Python · **Platform:** Windows, macOS, Linux desktop · **App type:** Local document comparison and clustering view

First-release learning implementation, with explicit scope below. This is one independently runnable app, not a placeholder in a combined repository.

## Features

- UTF-8 .txt/.md folder import
- Cosine ranking
- Threshold clusters
- Top 500 document pairs

## Requirements

Python 3.11+ with Tkinter; no pip packages.

## Quick start

```sh
git clone https://github.com/netcodermike/document-similarity-explorer.git
cd document-similarity-explorer
python app.py
```

Commands run from the repository root. Lines marked for a particular operating system apply only there. Language tools are prerequisites, not installed by the app. Close desktop windows normally; terminal/server apps stop with Ctrl+C unless their usage notes say otherwise.

## Example workflow

Choose a folder with two similar text files and one unrelated file. Compare at threshold 0.8, then lower it and inspect cluster count.

## Architecture, configuration, and data

app.py tokenizes words of length two or more, builds smoothed TF-IDF vectors, normalizes them, and computes all document pairs. Union-find-like linking groups pairs above a chosen 0–1 threshold. Tkinter displays ranked pairs and cluster count. Limits are 200 immediate files and 1 MiB per file. Self-tests compare identical/unrelated documents, empty vectors, and clusters. No originals or caches are written.

## Verification

Build with the quick-start command where needed, then run:

```sh
python app.py --self-test
```

Manual acceptance: Choose a folder with two similar text files and one unrelated file. Compare at threshold 0.8, then lower it and inspect cluster count. Also test malformed inputs and an unwritable output destination.

See [validation record](docs/VALIDATION.md) for observed checks and their limits. CI results verify only what the workflow runs; they do not establish native GUI correctness or production readiness.

## Limitations and next steps

Lexical similarity, not semantic meaning, plagiarism detection, or authorship proof. No PDF/DOCX, recursive folders, stemming, stop-word removal, cluster member view, or export. All-pairs work is quadratic and synchronous; the threshold groups transitively.

## Troubleshooting

Use the exact platform/toolchain above. Preserve originals and use synthetic fixtures first. Errors are displayed in the UI or stderr. A headless machine can run the model tests but cannot verify native GUI/audio behavior. Output paths are chosen explicitly; keep backups of important data.

## Source map

- `app.py`

## Development and license

Read [contributing](CONTRIBUTING.md) before changing the app, and [security/privacy](SECURITY.md) before supplying private data. Use synthetic fixtures for tests. No telemetry, paid API key, or account is required by the app itself. Dependencies, when present, are stated in Requirements.

[MIT license](LICENSE), copyright 2026 netcodermike.
