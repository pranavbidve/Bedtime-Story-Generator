import os
from openai import OpenAI
from dotenv import load_dotenv
# from generate import generate_story

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_model(prompt: str, max_tokens=30, temperature=0.1) -> str:
    # please use your own openai api key here.
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return resp.choices[0].message.content 
