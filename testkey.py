import sys

from openai import OpenAI, RateLimitError

from key_loader import load_api_key


try:
    api_key = load_api_key()
except RuntimeError as exc:
    sys.exit(str(exc))

client = OpenAI(api_key=api_key)

try:
    response = client.responses.create(
        model="gpt-4o-mini",
        input="Schreibe ein kurzes Haiku über KI.",
        store=True,
    )
except RateLimitError:
    print("OpenAI-Quota erreicht: Bitte prüfe dein OpenAI-Konto auf Billing/Plan oder warte bis das Kontingent wieder freigegeben ist.")
    sys.exit(1)
except Exception as exc:  # noqa: BLE001
    print(f"Fehler: {exc}")
    sys.exit(1)

print(response.output_text)