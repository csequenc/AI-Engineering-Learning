import os
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
from groq import Groq
import re

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai?")

client = Groq(api_key=my_api_key)
model = "qwen/qwen3.8-27b"

def get_product_price(product):
    if product == "iPhone 17":
        return 1000
    elif product == "iPhone 15":
        return 800
    else: 
        return 0
    
def calculator(expression):
    try:
        # Evaluate the expression safely
        result = eval(expression)
        return result
    
    except:
        return "calc error"
    
tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}

system_prompt = """
You are a shopping assistant.

DO NOT use native tool/function calling.
DO NOT output a structured tool call.
You must ONLY output normal text.

You have these tools available to you:

get_product_price(product)
calculator(expression)

Important:
Call tools exactly like these examples:

Action: get_product_price("iPhone 17")
Action: calculator("5000 - 1000")

Never write:
get_product_price(product="iPhone 17") or calculator(expression="5000 - 1000")

Follow these steps:
1. Decide what you need to do next.
2. Call ONLY one tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you recieve an Observation.
6. Then decide your next action.
7. When the task is completed, give the final answer.

Format:
Thought: What you need to do.
Action: tool_name(argument)

When finished:

Final Answer: your answer
"""

def run_agent(question):
    
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]
    
    for step in range(5):

        print("\n--------------------------------")
        print(f"Step {step + 1}")
        print("--------------------------------")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )

        answer = response.choices[0].message.content

        print(answer)

        # Agent has finished
        if "Final Answer:" in answer:
            break

        # Extract action
        match = re.search(
            r'Action:\s*(\w+)\("?(.*?)"?\)',
            answer
        )

        if not match:
            print("No valid action found.")
            break

        tool_name = match.group(1)
        tool_input = match.group(2)

        # Check tool
        if tool_name in tools:

            tool = tools[tool_name]

            observation = tool(tool_input)

        else:

            observation = f"Tool {tool_name} not found."

        print(f"Observation: {observation}")

        # Add assistant response
        messages.append({
            "role": "assistant",
            "content": answer
        })

        # Add observation
        messages.append({
            "role": "user",
            "content": f"Observation: {observation}"
        })

        sleep(5) # Wait for 5 seconds before the next step

prompt = """
I have 5000 Rupees. What is the price of iphone 17 ?
and how much money will I have left ?
"""
run_agent(prompt)

# models = client.models.list()

# for model in models.data:
#     print(model.id)