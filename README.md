# FlowTask

FlowTask is a small, configuration-driven task runner for building repeatable text pipelines.

## Install

```bash
pip install -e .
```

## Quickstart

Create a file named `pipeline.yml` (the input file must already exist):

```yaml
pipeline:
  name: "demo"
  tasks:
    - id: "read"
      type: read_text
      path: "./input.txt"

    - id: "upper"
      type: transform
      plugin: "builtin:uppercase"
      input: "@read.text"

    - id: "write"
      type: write_text
      path: "./out.txt"
      input: "@upper.text"
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

## CLI

- `flowtask execute --config-file <file>` runs a pipeline (.yml/.yaml/.json)
- `flowtask validate --config-file <file>` checks configuration without running it
- `flowtask plugins` lists built-in plugins
- Add `--quiet` to suppress non-error output

## Configuration notes

- Root key is `pipeline` with a `name` and a list of `tasks`.
- Each task needs a unique `id` and a `type` of `read_text`, `write_text`, or `transform`.
- Use `@<task>.<field>` to reference prior outputs (for example `@read.text`).
- Built-in transform plugins are `builtin:uppercase`, `builtin:lowercase`, and `builtin:replace` (requires `params.pattern` and `params.repl`).
- Config files must be `.yml`, `.yaml`, or `.json`.

---

See [TUTORIAL.md](TUTORIAL.md) for a longer walkthrough.
