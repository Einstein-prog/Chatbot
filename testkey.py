import sys

from openai import OpenAI, RateLimitError

from key_loader import load_api_key


def main() -> int:
    try:
        api_key = load_api_key()
    except RuntimeError as exc:
        print(exc)
        return 1

    client = OpenAI(api_key=api_key)
    prompt = 'Schreibe ein kurzes Haiku über KI.'

    try:
        response = client.responses.create(
            model='gpt-4o-mini',
            input=prompt,
            max_output_tokens=100,
        )
    except RateLimitError as exc:
        print(
            'OpenAI-Quota erreicht: Bitte prüfe dein OpenAI-Konto auf Billing/Plan oder warte bis das Kontingent wieder freigegeben ist.'
        )
        print(f'Fehlerdetails: {exc}')
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f'Fehler beim Testen des OpenAI-Schlüssels: {exc}')
        return 1

    print('OpenAI-Verbindung erfolgreich!')
    print('Antwort des Modells:')
    print(response.output_text)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
