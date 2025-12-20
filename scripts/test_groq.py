# Alternative: Use Groq API (even smarter - no downloads needed!)

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_sql_groq(prompt):
    """Use Groq API for SQL generation (fast and free)"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=200
    )
    return response.choices[0].message.content

def test_groq():
    """Test Groq API connection"""
    print("Testing Groq API...")
    
    test_prompt = "Generate SQL: SELECT * FROM trade LIMIT 5"
    result = generate_sql_groq(test_prompt)
    
    print(f"\nPrompt: {test_prompt}")
    print(f"Response: {result}")
    print("\nGroq API working!")

if __name__ == "__main__":
    test_groq()
