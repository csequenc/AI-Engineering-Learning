import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(
    api_key=my_api_key
)

model = "openai/gpt-oss-20b"
role = "user"

class Ticket(BaseModel):
    name: str
    product: str
    issue: str
    address: str
    email: str
    phone_number: str

schema = Ticket.model_json_schema()

response_format = {"type" : "json_object"}

system_prompt = f"""You are a helpful assistant that extracts personal information from customer tickets.
The information should be extracted in the following JSON format: {schema}"""

message_system = {"role": "system", "content": system_prompt}

text = "Hello, My name is Peter Leko. I have purchased an IPhone 15 Pro Max which stopped working after 2 days. I want to return it and get a refund. My address is Delhi, India. My email is peterleko@example.com. My phone number is 9876543210. Please help me with the return and refund process."
prompt = f"""This is a customer ticket. Please extract the personal information from the text and return it {text}"""
messages = [
    message_system,
    {"role": role, "content": prompt}
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format
)

answer = response.choices[0].message.content

print("Extracted Personal Information:")
print(answer)

# Iss Json ko padhte kaise hainn ====>

import json
raw_json = answer
data_file = json.loads(raw_json)

ticket = Ticket(**data_file)
print("Name:", ticket.name)
print("\nProduct:", ticket.product)
print("\nIssue:", ticket.issue)
print("\nAddress:", ticket.address)
print("\nEmail:", ticket.email)
print("\nPhone Number:", ticket.phone_number)


