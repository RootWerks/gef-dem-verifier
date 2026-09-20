import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from harness.supervisor_poc import GEFDEMSupervisorPoC
from schema.smf_tombstone import SMF_TOMBSTONE_LEN

def run_evaluation():
    supervisor = GEFDEMSupervisorPoC(delta_max_ms=10)

    test_vectors = [
        {
            "name": "vector_a_rogue_mutate",
            "payload": {
                "A_semantic": "MULTI_ASID_MUTATE",
                "delta_ms": 24,
                "E_token": "VALID_LEASE_0xF9",
                "R_t": "EPOCH_DRIFT_DETECTED",
                "ASID": "0x00B2",
                "JOBNAME": "ROGUEAGT"
            },
            "expected_verdict": "BITE",
            "expected_disp": "0xF505",
            "expected_len": SMF_TOMBSTONE_LEN
        },
        {
            "name": "vector_b_safe_read",
            "payload": {
                "A_semantic": "LOCAL_READ_AUDIT",
                "delta_ms": 3,
                "E_token": "VALID_LEASE_0xF9",
                "R_t": "EPOCH_SYNCHRONIZED",
                "ASID": "0x00A1",
                "JOBNAME": "SAFEAGENT"
            },
            "expected_verdict": "CLEAR",
            "expected_disp": None,
            "expected_len": None
        }
    ]

    for tv in test_vectors:
        res = supervisor.evaluate_and_audit(tv["payload"])
        verdict = res["verdict"]
        assert verdict == tv["expected_verdict"], f"[{tv['name']}] Verdict mismatch: got {verdict}, expected {tv['expected_verdict']}"
        
        if verdict == "BITE":
            rec = res["audit_record"]
            assert rec["DISP"] == tv["expected_disp"], f"[{tv['name']}] Disp mismatch: got {rec['DISP']}, expected {tv['expected_disp']}"
            assert rec["PACKED_BYTE_LENGTH"] == tv["expected_len"], f"[{tv['name']}] Byte len mismatch: got {rec['PACKED_BYTE_LENGTH']}, expected {tv['expected_len']}"
            print(f"PASS: {tv['name']} -> BITE verified (139-byte binary record packed cleanly)")
        else:
            print(f"PASS: {tv['name']} -> CLEAR verified (RRS 2PC PREPARE precondition met)")

    print("All multi-vector verification gates PASSED.")

if __name__ == "__main__":
    run_evaluation()
