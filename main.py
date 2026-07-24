from openai import OpenAI
from key_loader import load_api_key


api_key = load_api_key()
client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-5.4-mini",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)