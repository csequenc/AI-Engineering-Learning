from dotenv import load_dotenv
from pathlib import Path
from groq import Groq
import os

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API key kaha hai bhai?")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-20b"

# Step-1 
knowledge_base = {
    "age": "My dog is 5 years old.",
    "name": "My dog's name is Buddy."
}

# Step-2
def retrieve_info(question):
    question_lower = question.lower()
    if "age" in question_lower:
        return knowledge_base["age"]
    elif "name" in question_lower:
        return knowledge_base["name"]
    else:
        return None

def ask_llm(question):
    
    context = retrieve_info(question)
    
    sys_prompt = f"Write in one line only. Answer only on the basis of given context. Dont Hallucinate and dont try to answer from your knowledge, You can just take knowledge from the context. Context: {context}"
    
    system_message = {
        "role": "system",
        "content": sys_prompt
    }

    
    message = {
        "role": "user",
        "content": question
    }
    messages = [system_message, message]

    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer

question = "What is the the area of a football field?"
print(ask_llm(question))