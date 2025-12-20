# SQL prompt builder for question-to-SQL conversion

from pathlib import Path

class SQLPromptBuilder:
    def __init__(self):
        prompt_path = Path(__file__).parent.parent / "prompts" / "sql_generation.txt"
        with open(prompt_path, 'r', encoding='utf-8') as f:
            self.base_prompt = f.read()
    
    def build_prompt(self, question):
        # Build complete prompt with user question
        return f"{self.base_prompt}\n\nUser Question: {question}\n\nSQL:"
    
    def extract_sql(self, response):
        # Extract SQL from model response
        import re
        
        sql = response.strip()
        
        # Remove markdown code blocks if present
        if '```sql' in sql:
            sql = sql.split('```sql')[1].split('```')[0].strip()
        elif '```' in sql:
            sql = sql.split('```')[1].split('```')[0].strip()
        
        # Remove any explanatory text after the query
        if '\n\n' in sql:
            sql = sql.split('\n\n')[0].strip()
        
        # If doesn't start with SELECT, try to extract SELECT statement
        if not sql.upper().startswith('SELECT'):
            match = re.search(r'SELECT.*?;', sql, re.IGNORECASE | re.DOTALL)
            if match:
                sql = match.group(0)
        
        # Remove everything after first semicolon
        if ';' in sql:
            sql = sql.split(';')[0] + ';'
        else:
            sql += ';'
        
        return sql

