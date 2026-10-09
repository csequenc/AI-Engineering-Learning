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

def llm_ans(prompt):
    messages = [
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    ans = response.choices[0].message.content
    return ans

bad_prompt = """
This is a user complaint:
My laptop is not working properly. It keeps freezing and crashing. I have tried restarting it multiple times, but the problem persists. I need a solution as soon as possible.
Classify This.
"""
# print(llm_ans(bad_prompt))

good_prompt = """
#ROLE: You are a support assistant at a mobile company.
#TASK: You have to classify this issue in a category.
#CONSTRAINTS: You must classify the issue into one of the following categories: Billing, Technical, Return.
#OUTPUT_FORMAT: Your answer should be one word only and should be from the following options: Billing, Technical, Return.
#EXAMPLE: For instance if the user says "I was charged twice for my last bill", you should respond with "Billing".
#FALLBACK: If you are not sure about the category, you should respond with "OTHER".

This is a user complaint:
My laptop is not working properly. It keeps freezing and crashing. I have tried restarting it multiple times, but the problem persists. I need a solution as soon as possible.
Classify This.
"""

print(llm_ans(good_prompt))