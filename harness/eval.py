import sys
import json

PROHIBITED_CATEGORIES = {"prohibited_leak", "untrusted_asid"}

def evaluate(row):
    delta = row["delta"]
    delta_max = row["delta_max"]
    witness_valid = bool(row["witness_token"]) and row["revocation_list_valid"]
    cat_ok = row["semantic_category"] not in PROHIBITED_CATEGORIES
    
    return (delta <= delta_max) and witness_valid and cat_ok

if __name__ == "__main__":
    line = sys.stdin.read().strip()
    if not line:
        sys.exit(0)
    data = json.loads(line)
    passed = evaluate(data)
    expected = data.get("expect_pass", True)
    
    match = (passed == expected)
    status_str = "MATCH" if match else "MISMATCH"
    print(f"[{status_str}] Observed: {'PASS' if passed else 'FAIL'} | Expected: {'PASS' if expected else 'FAIL'}")
    sys.exit(0 if match else 1)
