import os
from pathlib import Path


def load_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key

    key_file = Path(__file__).with_name("openai.key")
    if key_file.exists():
        content = key_file.read_text(encoding="utf-8").strip()
        if content.startswith("api_key="):
            api_key = content.split("=", 1)[1].strip().strip('"').strip("'")
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                return api_key

    raise RuntimeError(
        "OPENAI_API_KEY is not set. Please export your OpenAI API key or place it in openai.key."
    )
