import os
from pathlib import Path


def _read_key_from_file(key_path: Path) -> str | None:
    if not key_path.exists():
        return None

    content = key_path.read_text(encoding="utf-8").strip()
    if not content:
        return None

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key in {"OPENAI_API_KEY", "api_key"} and value:
            return value

    return None


def load_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key

    candidates = [
        Path(__file__).resolve().parent / ".env",
        Path(__file__).resolve().parent / "openai.key",
        Path.cwd() / ".env",
        Path.cwd() / "openai.key",
        Path.home() / ".env",
        Path.home() / "openai.key",
        Path(__file__).resolve().parent.parent / "openai.key",
    ]

    for key_path in candidates:
        api_key = _read_key_from_file(key_path)
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            return api_key

    raise RuntimeError(
        "OPENAI_API_KEY is not set. Please export your OpenAI API key, add it to .env, or place it in openai.key."
    )
