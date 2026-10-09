import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(
    api_key=my_api_key
)

model = "openai/gpt-oss-20b"
role = "user"
prompt = "Suggest a name for a pizza outlet"
message_system = "You are a brand manager for my food company. Suggest only one name "

messages = [
    {"role": "system", "content": message_system},
    {"role": role, "content": prompt}
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=1.4,
)

print(response.choices[0].message.content)
