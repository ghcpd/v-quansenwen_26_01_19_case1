# FlowTask

FlowTask is a small, configuration-driven task runner for building repeatable text pipelines.

## Install

```bash
pip install -e .
```

## Quickstart

Create a file named `pipeline.yml`:

```yaml
pipeline:
  name: "demo"
  tasks:
    - id: "read"
      type: read_text
      path: "./input.txt"

    - id: "transform"
      type: transform
      plugin: "builtin:uppercase"
      input: "@read.text"

    - id: "write"
      type: write_text
      path: "./out.txt"
      input: "@transform.text"
```

Create an input file `input.txt`:

```text
Hello world
```

Run it:

```bash
flowtask execute --config-file pipeline.yml
```

Expected output:

```text
Executed pipeline: demo
Tasks: 3
```

The file `out.txt` will contain `HELLO WORLD`.

## CLI

- `flowtask execute --config-file <file>` executes a pipeline
- `flowtask validate --config-file <file>` checks configuration
- `flowtask plugins` lists built-in plugins

## Configuration notes

- You can reference prior task outputs using `@<task_id>.<field>` (for example `@read.text` where `read` is the task's `id`).
- `transform` steps support these plugins: `builtin:uppercase`, `builtin:lowercase`, and `builtin:replace`.

---

See [TUTORIAL.md](TUTORIAL.md) for a longer walkthrough.
