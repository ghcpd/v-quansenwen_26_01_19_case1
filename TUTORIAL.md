# Tutorial: Building a text pipeline

This tutorial walks through building a small text pipeline using FlowTask.

## 1) Initialize a pipeline

Create `pipeline.yml`:

```yaml
workflow:
  name: "book"
  steps:
    - name: "source"
      type: read_text
      path: "./book.txt"

    - name: "clean"
      type: transform
      plugin: replace
      input: "@source.text"
      params:
        pattern: "\t"
        repl: " "

    - name: "caps"
      type: transform
      plugin: uppercase
      input: "@clean.text"

    - name: "save"
      type: write_text
      path: "./book.cleaned.txt"
      input: "@caps.text"
```

Validate:

```bash
flowtask validate --config pipeline.yml
```

Run:

```bash
flowtask run --config pipeline.yml
```

## 2) Listing plugins

```bash
flowtask plugins
```

You should see `uppercase`, `lowercase`, and `replace`.

## 3) JSON config

You can also use JSON:

```bash
flowtask run --config pipeline.json
```

## 4) Concurrency

By default FlowTask runs with 4 workers. You can reduce it:

```bash
flowtask run --config pipeline.yml --workers 1
```
