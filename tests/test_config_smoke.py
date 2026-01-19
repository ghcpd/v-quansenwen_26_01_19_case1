from flowtask.config import parse_pipeline


def test_parse_pipeline_minimal():
    spec = parse_pipeline(
        {
            "pipeline": {
                "name": "demo",
                "tasks": [
                    {"id": "read", "type": "read_text", "path": "in.txt"},
                    {
                        "id": "up",
                        "type": "transform",
                        "plugin": "builtin:uppercase",
                        "input": "@read.text",
                    },
                    {"id": "write", "type": "write_text", "path": "out.txt", "input": "@up.text"},
                ],
            }
        }
    )

    assert spec.name == "demo"
    assert [t.id for t in spec.tasks] == ["read", "up", "write"]
