import os
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hain bhai?")

client = Groq(api_key=my_api_key)

groqmodel = "openai/gpt-oss-20b"
model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "Employees receive 24 days of paid leave per year.",
    "Employees work from the office on Tuesday, Wednesday, and Thursday, and optional work from home on Monday and Friday.",
    "Employees are required to work a standard 40-hour work week.",
    "Employees recieve Rs. 5000 as a monthly allowance for internet and electricity bills.",
    "Employees are required to attend a mandatory meeting every month.",
    "Employees have a notice period of 90 days",
    "Employees are entitled to health insurance coverage.",
    "Employees recieve Rs. 3000 as a monthly allowance for transportation.",
    "Employees recieve Rs. 2000 as a monthly allowance for gym membership.",
]

document_embeddings = model.encode(documents)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve(query_embedding):
    scores = []

    for i, document in enumerate(document_embeddings):
        score = cosine_similarity(query_embedding, document)
        scores.append((score, documents[i]))

    scores.sort(reverse=True)

    return scores[0]

def ask_llm(question,context):
    
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

    response = client.chat.completions.create(model=groqmodel, messages=messages)
    answer = response.choices[0].message.content
    return answer
    

query = "What is the standard work week for employees?"
query_embedding = model.encode(query)
score, context = retrieve(query_embedding)
answer = ask_llm(query,context)
print(f"Score: {score}, Context: {context}")