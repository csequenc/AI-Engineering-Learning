from dotenv import load_dotenv
from pathlib import Path
from groq import Groq
import os

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API key kahan hai bhai ?")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-20b"

prompt = "Write a short story about a robot learning to love."
message ={
    "role": "user",
    "content": prompt
}

messages = [message]

# response = client.chat.completions.create(model=model, messages=messages)
# answer = response.choices[0].message.content
# print("Response from the model:", answer)

stream_response = client.chat.completions.create(model=model, messages=messages, stream=True)

for chunk in stream_response:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
        

