# Phase 4 Complete Integration Test
# Pipeline: Question -> SQL -> Execute -> Validate -> Groq Fix -> Retry -> Format

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import ModelLoader
from src.prompt_builder import SQLPromptBuilder
from src.executor import QueryExecutor
from src.formatter import ResponseFormatter
from src.groq_client import GroqClient


class GroqFixer:
    # Wrapper for Groq SQL fixing with error context
    
    def __init__(self, groq: GroqClient):
        self.groq = groq
        self.last_error = ""
        self.last_sql = ""
    
    def fix(self, question: str) -> str:
        return self.groq.fix_sql(question, self.last_sql, self.last_error)


def test_phase4():
    # Test complete chatbot pipeline with all validations
    
    print("Phase 4 Complete Pipeline Test\n")
    print("Loading models...")
    
    model = ModelLoader()
    model.load_sql_generator()
    
    builder = SQLPromptBuilder()
    executor = QueryExecutor(max_retries=2, log_failures=False)
    formatter = ResponseFormatter()
    groq = GroqClient()
    fixer = GroqFixer(groq)
    
    # Test questions
    test_questions = [
        "Total imports in 2080?",
        "Top 5 countries by trade value?",
        "Monthly imports in 2081?",
        "Trade with country ZZ?",
        "How many unique countries?",
    ]
    
    print(f"\nTesting {len(test_questions)} questions:\n")
    
    passed = 0
    
    for i, question in enumerate(test_questions, 1):
        print(f"[{i}] Question: {question}")
        
        # Phase 2: Mistral generates SQL
        prompt = builder.build_prompt(question)
        sql = model.generate_sql(prompt)
        clean_sql = builder.extract_sql(sql)
        print(f"    Phase 2 - SQL: {clean_sql[:50]}...")
        
        # Phase 3: Execute with Groq fixing on error
        fixer.last_sql = clean_sql
        success, result, msg = executor.execute(clean_sql, question, fixer.fix)
        
        if not success:
            fixer.last_error = msg
            print(f"    Phase 3 - Error: {msg}")
            print()
            continue
        
        regen_note = " (Groq fixed)" if "Regenerated" in msg else ""
        print(f"    Phase 3 - Executed: {msg}{regen_note}")
        
        # Groq validates result
        is_valid = groq.validate_sql(question, clean_sql, result)
        if is_valid:
            print(f"    Groq validated: PASS")
        else:
            print(f"    Groq validated: FAIL")
        
        # Phase 4: TinyLlama formats response
        answer = formatter.format_result(question, clean_sql, result)
        print(f"    Phase 4 - Answer: {answer}")
        print()
        
        passed += 1
    
    print(f"Results: {passed}/{len(test_questions)} passed")
    print("Phase 4 complete")


if __name__ == "__main__":
    test_phase4()
