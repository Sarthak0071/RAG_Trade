# SQL accuracy test with real data execution and Groq validation

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import ModelLoader
from src.prompt_builder import SQLPromptBuilder
from src.database import TradeDatabase
from src.groq_client import GroqClient
from tests.test_data import TEST_CASES

def test_with_real_data():
    # Load Mistral
    print("Loading Mistral-7B SQL generator...\n")
    loader = ModelLoader()
    loader.load_sql_generator()
    
    prompt_builder = SQLPromptBuilder()
    groq = GroqClient()
    
    total = len(TEST_CASES)
    passed = 0
    failed_cases = []
    
    print(f"Testing {total} questions with REAL DATA validation\n")
    
    with TradeDatabase() as db:
        for i, test in enumerate(TEST_CASES, 1):
            question = test["question"]
            
            print(f"\n[{i}/{total}] {question}")
            
            # 1. Mistral generates SQL
            prompt = prompt_builder.build_prompt(question)
            response = loader.generate_sql(prompt)
            sql = prompt_builder.extract_sql(response)
            
            print(f"SQL: {sql}")
            
            # 2. Execute on REAL data
            try:
                result = db.execute_query(sql)
                result_preview = result.head(5).to_string() if not result.empty else "No results"
                print(f"Results: {result_preview[:200]}...")
            except Exception as e:
                print(f"ERROR executing SQL: {e}")
                failed_cases.append({"question": question, "sql": sql, "error": str(e)})
                continue
            
            # 3. Groq validates with ACTUAL results
            try:
                is_correct, reason = groq.validate_sql(question, sql, result_preview)
                if is_correct:
                    print("PASS (Groq validated)")
                    passed += 1
                else:
                    print(f"FAIL: {reason}")
                    failed_cases.append({"question": question, "sql": sql, "reason": reason})
            except Exception as e:
                print(f"Groq validation error: {e}")
                failed_cases.append({"question": question, "sql": sql, "error": str(e)})
    
    # Results
    accuracy = (passed / total) * 100
    print(f"\n\nFINAL RESULTS")
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Accuracy: {accuracy:.1f}%")
    
    if accuracy >= 90:
        print(f"\nSUCCESS: {accuracy:.1f}% accuracy achieved")
        return 0
    else:
        print(f"\nNeed improvement: {accuracy:.1f}% (target: 90%)")
        if failed_cases and len(failed_cases) <= 10:
            print("\nFailed cases:")
            for case in failed_cases[:10]:
                print(f"  - {case['question']}")
                if 'reason' in case:
                    print(f"    {case['reason']}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(test_with_real_data())
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
