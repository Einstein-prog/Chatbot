# Chatbot

Dieses Projekt enthält einen OpenAI-Chatbot mit einer einfachen Gradio-Weboberfläche.

## Setup

1. Kopiere `.env.example` zu `.env` und trage dort deinen OpenAI-API-Key ein:
   ```
   OPENAI_API_KEY=dein_api_key
   ```
2. Installiere die Abhängigkeiten mit `pip install -r requirements.txt`.
3. Starte die App mit `python main.py`.
4. Öffne die angezeigte URL im Browser, z. B. `http://127.0.0.1:7860`.

## Funktionen

- Chat über eine Browseroberfläche mit Gradio
- Auswahl zwischen mehreren OpenAI-Modellen
- Anzeige des aktuellen OpenAI-Quota-/Fehlerstatus direkt in der UI

## Sicherheitshinweis

Die Datei `.env` enthält Secrets und sollte niemals in GitHub gepusht werden.
