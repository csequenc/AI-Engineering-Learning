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

# 3 Prompts
prompt1 = "Hi"
prompt2 = "Explain time travel in detail."
prompt3 = "What is the meaning of life in 1000 words - Essay Writing."

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
        
    messages = [
        {"role": role, "content": prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=5000
    )
    
    usage = response.usage
    print(f"Prompt: {prompt} --> Tokens Used: {usage.total_tokens}, Prompt Tokens: {usage.prompt_tokens}, Completion Tokens: {usage.completion_tokens}, Finish Reason: {response.choices[0].finish_reason}")
    
    
