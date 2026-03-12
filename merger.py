from pathlib import Path


def walk(dir_name: str, report_name: str):
    result_parts = []
    root = Path(dir_name)
    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(part in IGNORE for part in path.parts):
            continue

        text = path.read_text(encoding="utf-8").strip()
        result_parts.append(f"{path.absolute()}:\n{text}\n\n")

    result = "".join(result_parts)
    Path(report_name).unlink(missing_ok=True)
    Path(report_name).write_text(result, encoding="utf-8")


IGNORE = [
    "__pycache__",
    ".idea",
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "alembic",
    "__init__.py",
    # ".env.dev",
    # ".env.local",
    # ".env.prod",
    "filebeat.yml",
    "merger.py",
    "README.md",
    "uv.lock",
    "res.txt"
]

walk("./", "res.txt")
