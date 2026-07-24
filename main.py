import sys

from openai import OpenAI, RateLimitError
from key_loader import load_api_key


try:
    api_key = load_api_key()
except RuntimeError as exc:
    sys.exit(str(exc))

client = OpenAI(api_key=api_key)

print("Verfügbare Modelle:")
print("1) gpt-4o-mini")
print("2) gpt-4o")
print("3) gpt-3.5-turbo")
print("4) gpt-5.4-mini")

while True:
    choice = input("Wähle ein Modell (1-4): ").strip()
    if choice == "1":
        model = "gpt-4o-mini"
        break
    if choice == "2":
        model = "gpt-4o"
        break
    if choice == "3":
        model = "gpt-3.5-turbo"
        break
    if choice == "4":
        model = "gpt-5.4-mini"
        break
    print("Ungültige Auswahl. Bitte 1, 2, 3 oder 4 eingeben.")

print(f"Chat gestartet mit {model}. Tippe 'beenden' zum Beenden.")

while True:
    prompt = input("Du: ").strip()

    if prompt.lower() in {"", "beenden", "exit", "quit"}:
        print("Chat beendet.")
        break

    try:
        response = client.responses.create(
            model=model,
            input=prompt,
        )
    except RateLimitError:
        print(
            "OpenAI-Quota erreicht: Bitte prüfe dein OpenAI-Konto auf Billing/Plan oder warte bis das Kontingent wieder freigegeben ist."
        )
        break

    print(f"Chatbot: {response.output_text}")