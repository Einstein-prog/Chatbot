import os
import socket
import sys

import gradio as gr
from openai import OpenAI, RateLimitError

from key_loader import load_api_key


try:
    api_key = load_api_key()
except RuntimeError as exc:
    sys.exit(str(exc))

client = OpenAI(api_key=api_key)
MODELS = [
    ("gpt-4o-mini", "gpt-4o-mini"),
    ("gpt-4o", "gpt-4o"),
    ("gpt-3.5-turbo", "gpt-3.5-turbo"),
    ("gpt-5.4-mini", "gpt-5.4-mini"),
]
def find_free_port(start_port: int = 7860, max_port: int = 7999) -> int:
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("Keine freien lokalen Ports gefunden")


def build_quota_html(status: str, detail: str, percent: int = 60) -> str:
    if status == "ok":
        color = "#22c55e"
        label = "OpenAI-Quota: verfügbar"
        percent = 100
    elif status == "warning":
        color = "#f59e0b"
        label = "OpenAI-Quota: eingeschränkt"
        percent = 70
    else:
        color = "#ef4444"
        label = "OpenAI-Quota: erschöpft"
        percent = 100

    return f"""
    <div style="margin-bottom: 10px; font-family: Arial, sans-serif;">
      <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 14px;">
        <strong>{label}</strong>
        <span>{detail}</span>
      </div>
      <div style="width: 100%; height: 12px; background: #e5e7eb; border-radius: 999px; overflow: hidden;">
        <div style="width: {percent}%; height: 100%; background: {color}; border-radius: 999px;"></div>
      </div>
    </div>
    """


def chat_with_model(prompt: str, model: str, usage_count: int) -> tuple[str, int, str]:
    if not prompt or not prompt.strip():
        return "Bitte gib eine Nachricht ein.", usage_count, build_quota_html("warning", "keine Anfrage gesendet", 30)

    try:
        response = client.responses.create(
            model=model,
            input=prompt.strip(),
        )
        answer = response.output_text
        return (
            answer,
            usage_count + 1,
            build_quota_html("ok", "Letzte Anfrage erfolgreich an OpenAI gesendet", 100),
        )
    except RateLimitError as exc:
        error_code = getattr(exc, "code", None)
        if error_code == "insufficient_quota":
            detail = "OpenAI meldet keine verfügbare Quota mehr"
            status = "error"
        else:
            detail = "OpenAI hat das Rate-Limit erreicht"
            status = "warning"
        return (
            "OpenAI-Quota erreicht: Bitte prüfe dein OpenAI-Konto auf Billing/Plan oder warte bis das Kontingent wieder freigegeben ist.",
            usage_count,
            build_quota_html(status, detail, 100),
        )
    except Exception as exc:  # noqa: BLE001
        return f"Fehler: {exc}", usage_count, build_quota_html("warning", "Fehler bei der Anfrage", 50)


with gr.Blocks(title="OpenAI Chatbot") as demo:
    gr.Markdown("# OpenAI Chatbot")

    with gr.Row():
        model_dropdown = gr.Dropdown(
            choices=[name for name, _ in MODELS],
            value="gpt-4o-mini",
            label="Modell",
        )

    usage_state = gr.State(value=0)
    quota_box = gr.HTML(value=build_quota_html("warning", "Warte auf erste Anfrage", 40))

    prompt_box = gr.Textbox(
        lines=5,
        label="Deine Nachricht",
        placeholder="Stell eine Frage oder gib einen Text ein...",
    )
    output_box = gr.Textbox(lines=10, label="Antwort")
    submit_button = gr.Button("Senden")

    submit_button.click(
        chat_with_model,
        inputs=[prompt_box, model_dropdown, usage_state],
        outputs=[output_box, usage_state, quota_box],
    )
    prompt_box.submit(
        chat_with_model,
        inputs=[prompt_box, model_dropdown, usage_state],
        outputs=[output_box, usage_state, quota_box],
    )


if __name__ == "__main__":
    port = int(os.environ.get("GRADIO_SERVER_PORT", find_free_port()))
    demo.launch(server_name="0.0.0.0", server_port=port, inbrowser=True)