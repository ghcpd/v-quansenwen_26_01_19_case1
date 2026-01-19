# Tutorial: Building a text pipeline

This tutorial walks through building a small text pipeline using FlowTask.

## 1) Initialize a pipeline

Create `pipeline.yml`:

```yaml
pipeline:
  name: "book"
  tasks:
    - id: "source"
      type: read_text
      path: "./book.txt"

    - id: "clean"
      type: transform
      plugin: builtin:replace
      input: "@source.text"
      params:
        pattern: "\t"
        repl: " "

    - id: "caps"
      type: transform
      plugin: builtin:uppercase
      input: "@clean.text"

    - id: "save"
      type: write_text
      path: "./book.cleaned.txt"
      input: "@caps.text"
```

Validate:

```bash
flowtask validate --config-file pipeline.yml
```

Run:

```bash
flowtask execute --config-file pipeline.yml
```

## 2) Listing plugins

```bash
flowtask plugins
```

You should see `builtin:uppercase`, `builtin:lowercase`, and `builtin:replace`.

## 3) JSON config

You can also use JSON:

```bash
flowtask execute --config-file pipeline.json
```

