# Response formatter using Groq for reliable natural language output

import pandas as pd
import math
from src.groq_client import GroqClient


class ResponseFormatter:
    # Format query results into friendly natural language using Groq
    
    def __init__(self):
        self.groq = GroqClient()
    
    def format_result(self, question: str, sql: str, result: pd.DataFrame) -> str:
        # Format query result into friendly natural language
        
        # Handle empty results
        if result is None or result.empty:
            return "I couldn't find any data matching your query. Please try different filters."
        
        # Check for NaN single value
        if len(result) == 1 and len(result.columns) == 1:
            value = result.iloc[0, 0]
            if pd.isna(value) or (isinstance(value, float) and math.isnan(value)):
                return "No data found for this query."
        
        # Format data for prompt
        data_str = self._format_data(result)
        
        # Use Groq to generate friendly response
        prompt = f"""You are answering questions about Nepal trade data.

Question: {question}

Here is the actual data from the database:
{data_str}

Instructions:
- Use ONLY the exact numbers shown above
- Format currency as Rs with commas
- Answer the question directly and completely
- Be friendly and conversational

Your answer:"""
        
        response = self.groq.generate(prompt, temperature=0.1, max_tokens=300)
        return response.strip()
    
    def _format_data(self, result: pd.DataFrame) -> str:
        # Format DataFrame into readable string
        
        if len(result) == 1 and len(result.columns) == 1:
            # Single value
            value = result.iloc[0, 0]
            if isinstance(value, (int, float)) and not pd.isna(value):
                return f"Result: Rs {int(value):,}"
            return f"Result: {value}"
        
        if len(result) <= 15:
            # Multiple rows - show all with clear formatting
            lines = []
            for idx, row in result.iterrows():
                parts = []
                for col in result.columns:
                    val = row[col]
                    if isinstance(val, (int, float)) and not pd.isna(val):
                        parts.append(f"{col}={int(val):,}")
                    else:
                        parts.append(f"{col}={val}")
                lines.append(" | ".join(parts))
            return "Rows:\n" + "\n".join(lines)
        
        # Large result - show summary with first rows
        lines = []
        for idx, row in result.head(5).iterrows():
            parts = []
            for col in result.columns:
                val = row[col]
                if isinstance(val, (int, float)) and not pd.isna(val):
                    parts.append(f"{col}={int(val):,}")
                else:
                    parts.append(f"{col}={val}")
            lines.append(" | ".join(parts))
        return f"Total: {len(result)} rows\nFirst rows:\n" + "\n".join(lines)
