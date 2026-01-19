# FlowTask

FlowTask is a small, configuration-driven task runner for building repeatable text pipelines.

## Install

```bash
pip install -e .
```

## Quickstart

Create a file named `pipeline.yml`:

```yaml
workflow:
  name: "demo"
  steps:
    - name: "read"
      type: read_text
      path: "./input.txt"

    - name: "transform"
      type: transform
      plugin: uppercase
      input: "@read.text"

    - name: "write"
      type: write_text
      path: "./out.txt"
      input: "@transform.text"
```

Run it:

```bash
flowtask run --config pipeline.yml
```

Expected output:

```text
Loaded 3 steps
✅ write -> ./out.txt
```

## CLI

- `flowtask run --config <file>` runs a pipeline
- `flowtask validate --config <file>` checks configuration
- `flowtask plugins` lists built-ins

## Configuration notes

- You can reference prior outputs using `@<step>.<field>` (for example `@read.text`).
- `transform` steps support `uppercase`, `lowercase`, and `replace`.

---

See [TUTORIAL.md](TUTORIAL.md) for a longer walkthrough.
