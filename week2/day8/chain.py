import os
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai?")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-20b"

JD="""
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""
RESUME="""
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
"""

def ask_llm(system_prompt, user_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    ans = response.choices[0].message.content
    return ans

def extract_skills_from_resume(resume):
    system_prompt = """
You are a resume parser. You will be given a resume text and you need to extract the skills from it. The skills should be returned as a comma-separated list.

"""
    user_prompt = f"Resume:\n{resume}\n\nExtract the skills from the above resume."
    skills = ask_llm(system_prompt, user_prompt)
    return skills

def match_skills_with_job_description(job_description):
    system_prompt = """
You are a job matching assistant. You will be given a list of skills and a job description. You need to match the skills with the job description and return the matched skills as a comma-separated list.

"""
    user_prompt = f"Skills:Extract skills from the job description{job_description}"
    skills = ask_llm(system_prompt, user_prompt)
    return skills

def compare_skills(resume_skills, job_skills):
    system_prompt = """
    You are a skill comparison assistant. You will be given two lists of skills: one from a resume and one from a job description. Then you need to give a score between 1-100 and a short description why this candidate is a match or unfit for the particular job role. The score should be based on how many skills match between the two lists. If the candidate has all the required skills, the score should be 100. If the candidate has none of the required skills, the score should be 0. If the candidate has some of the required skills, the score should be between 1-99 based on how many skills match.
    """
    user_prompt = f"Resume Skills: {resume_skills}\nJob Description Skills: {job_skills}\n\nCompare the two lists of skills and give a score between 1-100 and a short description why this candidate is a match or unfit for the particular job role."
    comparison = ask_llm(system_prompt, user_prompt)
    return comparison

resume_skills = extract_skills_from_resume(RESUME)
job_skills = match_skills_with_job_description(JD)
comparison = compare_skills(resume_skills, job_skills)
print("Resume Skills:", resume_skills)
print("Job Description Skills:", job_skills)
print("Comparison:", comparison)