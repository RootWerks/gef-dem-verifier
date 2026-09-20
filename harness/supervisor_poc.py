import hashlib
import time
import json
import sys
import os

# Ensure repo root is discoverable for binary schema imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from schema.smf_tombstone import SMFTombstone, SMF_TOMBSTONE_LEN

class GEFDEMSupervisorPoC:
    def __init__(self, delta_max_ms: int = 10):
        self.delta_max_ms = delta_max_ms
        self.prohibited_categories = {
            "MULTI_ASID_MUTATE", 
            "EU_WORKPLACE_EMOTION_INFERENCE"
        }

    def _hash(self, val: str) -> bytes:
        return hashlib.sha256(val.encode("utf-8")).digest()

    def evaluate_and_audit(self, payload: dict) -> dict:
        delta = payload.get("delta_ms", 0)
        semantic = payload.get("A_semantic", "")
        e_token = payload.get("E_token", "")
        r_iss_raw = payload.get("R_iss", "root_iss_initial")
        r_prep_raw = payload.get("R_prep", "root_prep_transient")
        drift_status = payload.get("R_t", "EPOCH_SYNCHRONIZED")
        asid = payload.get("ASID", "0x00A1")
        jobname = payload.get("JOBNAME", "AGNTJOB1")[:8]

        # Core Enforcement Conjunction evaluation
        op1_valid = delta <= self.delta_max_ms
        witness_valid = bool(e_token) and (drift_status == "EPOCH_SYNCHRONIZED")
        cat_allowed = semantic not in self.prohibited_categories

        short_circuited = not (op1_valid and witness_valid and cat_allowed)

        if short_circuited:
            if not cat_allowed:
                subtype = 5
                disp_int = 0xF505
            else:
                subtype = 3
                disp_int = 0xF003

            # Construct binary tombstone model
            tombstone_obj = SMFTombstone(
                record_type=subtype,
                disposition=disp_int,
                delta_val=float(delta),
                r_iss=self._hash(r_iss_raw),
                r_prep=self._hash(r_prep_raw),
                delta_root=self._hash(str(delta)),
                e_token_hash=self._hash(e_token)
            )
            packed_binary = tombstone_obj.pack()

            # Diagnostic dict representation for debugging/CI output
            audit_dict = {
                "SMFLEN": 40 + SMF_TOMBSTONE_LEN,
                "SMFSTYP": f"0x0{subtype}",
                "SMFTOD": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "SMFSID": "SYP1",
                "ASID": asid,
                "JOBNAME": jobname,
                "DISP": f"0x{disp_int:04X}",
                "PACKED_BYTES_HEX": packed_binary.hex(),
                "PACKED_BYTE_LENGTH": len(packed_binary),
                "EXPECTED_LENGTH": SMF_TOMBSTONE_LEN,
                "STATUS": "HARD_ABORT_BYTE_ZERO_CEX_GATE"
            }
            return {"verdict": "BITE", "audit_record": audit_dict}

        # Clear precondition for RRS 2PC PREPARE
        return {
            "verdict": "CLEAR",
            "audit_record": None,
            "message": "Epistemic proof valid; cleared to touch RRS 2PC PREPARE."
        }


# --- Execution Harness ---
if __name__ == "__main__":
    supervisor = GEFDEMSupervisorPoC(delta_max_ms=10)

    vec_a = {
        "A_semantic": "MULTI_ASID_MUTATE",
        "delta_ms": 24,
        "E_token": "VALID_LEASE_0xF9",
        "R_t": "EPOCH_DRIFT_DETECTED",
        "ASID": "0x00B2",
        "JOBNAME": "ROGUEAGT"
    }

    vec_b = {
        "A_semantic": "LOCAL_READ_AUDIT",
        "delta_ms": 3,
        "E_token": "VALID_LEASE_0xF9",
        "R_t": "EPOCH_SYNCHRONIZED",
        "ASID": "0x00A1",
        "JOBNAME": "SAFEAGENT"
    }

    print("=== VECTOR A EVALUATION ===")
    print(json.dumps(supervisor.evaluate_and_audit(vec_a), indent=2))
    
    print("\n=== VECTOR B EVALUATION ===")
    print(json.dumps(supervisor.evaluate_and_audit(vec_b), indent=2))
