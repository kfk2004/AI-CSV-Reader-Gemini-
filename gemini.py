import google.generativeai as genai
import os
import pandas as pd
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.environ["API_KEY"] = "AIzaSyCxXxtaqNgK0Y9moR2QPb_5XaJcb3uQda4"

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")


csv_file_path = 'fakedatarev.csv'
data = pd.read_csv(csv_file_path)


def answer_question(user_input):
    data_summary = data.head().to_string()
    prompt = f"Data Overview:\n{data_summary}\n\nQuestion: {user_input}"
    response = model.generate_content(prompt)
    return response.text.strip()

class UserInput(BaseModel):
    user_input: str

@app.post('/api/ask')
async def ask_model(user_input: UserInput):
    response = answer_question(user_input.user_input)
    return {'response': response}

@app.get('/')
async def root():
    return {'example': 'This is an example', 'data': 0}
