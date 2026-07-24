from openai import OpenAI
from key_loader import load_api_key


client = OpenAI(api_key=load_api_key())

response = client.responses.create(
    model="gpt-5.4-mini",
    input="write a haiku about ai",
    store=True,
)

print(response.output_text)