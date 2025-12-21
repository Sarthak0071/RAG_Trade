# Groq API client wrapper

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    def __init__(self):
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
    
    def generate(self, prompt, temperature=0.7, max_tokens=1024):
        # Generate text using Groq API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    
    def validate_sql(self, question: str, sql: str, result_preview: str) -> tuple[bool, str]:
        # Validate if SQL correctly answers the question based on actual results
        
        prompt = f"""You are validating SQL queries for a trade database.

Question: {question}
Generated SQL: {sql}
Actual Results: {result_preview}

Does this SQL correctly answer the question? Consider:
1. Does it return the right data?
2. Does it use the correct columns?
3. Are the results reasonable?

BE LENIENT:
- Different formatting (aliases, line breaks) is OK
- If results look correct, SQL is correct
- Minor style differences are OK
- Focus on LOGIC, not formatting

Answer ONLY "YES" or "NO" with brief reason.

Format: YES/NO: reason
"""
        
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=100
        )
        
        answer = response.choices[0].message.content.strip()
        
        # Parse response
        if answer.startswith("YES"):
            return True, answer[4:].strip()
        else:
            return False, answer[3:].strip() if answer.startswith("NO") else answer
    
    def generate_test_questions(self, num_questions=50):
        # Generate test questions for trade data
        prompt = f"""Generate {num_questions} realistic questions about Nepal trade data for testing a SQL query system.

Data structure:
- Table: trade
- Columns: Year (2077-2082), Month (1-12), Direction (I/E), HS_Code, Description, Country (ISO-2), Value, Quantity, Unit, Revenue
- 760K records of Nepal import/export data

Generate diverse questions covering:
- Basic aggregations (SUM, COUNT, AVG)
- Filtering by year, country, commodity
- GROUP BY queries
- TOP N queries
- Complex multi-condition queries
- Time series and trends

Return ONLY the questions, one per line, no numbering.
"""
        
        response = self.generate(prompt, temperature=0.8, max_tokens=2048)
        questions = [q.strip() for q in response.split('\n') if q.strip() and not q.strip().startswith('#')]
        return questions[:num_questions]
    
    def fix_sql(self, question: str, bad_sql: str, error_msg: str) -> str:
        """
        Use Groq to fix broken SQL - reuses Mistral's prompt + error context.
        """
        # Load Mistral's prompt
        from pathlib import Path
        prompt_path = Path(__file__).parent.parent / "prompts" / "sql_generation.txt"
        with open(prompt_path, 'r', encoding='utf-8') as f:
            base_prompt = f.read()
        
        # Add error context
        fix_prompt = f"""{base_prompt}

PREVIOUS ATTEMPT FAILED:
SQL Generated: {bad_sql}
Error: {error_msg}

FIX THIS: The above SQL failed. Generate a corrected version that avoids this error.
Keep it simple and follow ALL the rules above.

User Question: {question}

SQL:"""
        
        fixed_sql = self.generate(fix_prompt, temperature=0.1, max_tokens=300)
        
        # Extract SQL
        if '```sql' in fixed_sql:
            fixed_sql = fixed_sql.split('```sql')[1].split('```')[0].strip()
        elif '```' in fixed_sql:
            fixed_sql = fixed_sql.split('```')[1].split('```')[0].strip()
        
        return fixed_sql
