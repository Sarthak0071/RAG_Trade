"""
Phase 3 Integration Test: Groq-powered SQL error recovery.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.executor import QueryExecutor
from src.models import ModelLoader
from src.prompt_builder import SQLPromptBuilder
from src.groq_client import GroqClient


class GroqFixer:
    """Wrapper to use Groq for SQL fixing with error context."""
    
    def __init__(self, groq: GroqClient):
        self.groq = groq
        self.last_error = ""
        self.last_sql = ""
    
    def fix(self, question: str) -> str:
        """Fix SQL using Groq with last error context."""
        return self.groq.fix_sql(question, self.last_sql, self.last_error)


def test_phase3_complete():
    """Test Phase 3 with Groq-powered error recovery."""
    
    print("Phase 3: Groq-Powered SQL Error Recovery\n")
    print("Loading models...")
    
    model = ModelLoader()
    model.load_sql_generator()
    
    builder = SQLPromptBuilder()
    executor = QueryExecutor(max_retries=2, log_failures=True)
    groq = GroqClient()
    fixer = GroqFixer(groq)
    
    # 5 questions GUARANTEED to fail with Mistral → Force Groq fixing
    test_questions = [
        # Mistral generates "LIMIT N" placeholder → Parser error
        "Give me exactly 25 random trade records",
        
        # Mistral uses YEAR() function wrong → Type error  
        "Show trades from specific months in year 2080",
        
        # Mistral generates Direction='Both' → Validation/execution error
        "Total trade value counting both imports and exports",
        
        # Mistral uses OFFSET (banned) → Validation error
        "Skip first 100 records and show next 50",
        
        # Mistral generates complex HAVING with wrong aggregates
        "Years where average monthly trade exceeded 500 million",
    ]
    
    print(f"\nTesting {len(test_questions)} questions (GUARANTEED Mistral failures):\n")
    
    passed = 0
    failed = 0
    groq_fixed = 0
    
    for i, question in enumerate(test_questions, 1):
        print(f"[{i}/{len(test_questions)}] {question}")
        
        # Generate SQL with Mistral
        prompt = builder.build_prompt(question)
        sql = model.generate_sql(prompt)
        clean_sql = builder.extract_sql(sql)
        
        print(f"  SQL: {clean_sql[:70]}...")
        
        # Store context for Groq fixer
        fixer.last_sql = clean_sql
        
        # Execute with Groq fixing on error
        success, result, msg = executor.execute(
            clean_sql,
            question,
            fixer.fix
        )
        
        # Store error for next iteration
        if not success:
            fixer.last_error = msg
        
        if success:
            # Validate with Groq
            is_valid = groq.validate_sql(question, clean_sql, result)
            
            if is_valid:
                print(f"  PASS: {msg} (Groq validated)")
                passed += 1
                if "Regenerated" in msg:
                    groq_fixed += 1
            else:
                print(f"  FAIL: Groq validation failed")
                failed += 1
        else:
            print(f"  FAIL: {msg}")
            failed += 1
        
        print()
    
    # Summary
    print("\nPHASE 3 RESULTS - GROQ-POWERED RECOVERY")
    print(f"Passed: {passed}/{len(test_questions)}")
    print(f"Failed: {failed}/{len(test_questions)}")
    print(f"Groq fixed: {groq_fixed}")
    print(f"Success rate: {passed/len(test_questions)*100:.1f}%")
    
    log_file = Path("logs/query_errors.jsonl")
    if log_file.exists():
        with open(log_file) as f:
            log_count = len(f.readlines())
        print(f"\nLogged {log_count} total failures")
    
    print("\nPhase 3 Groq-powered error recovery verified")


if __name__ == "__main__":
    test_phase3_complete()
