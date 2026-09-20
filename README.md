# GEF-DEM Verifier (z/OS Silicon Sovereignty)

[![CI Multi-Vector](https://github.com/RootWerks/gef-dem-verifier/actions/workflows/verify.yml/badge.svg)](https://github.com/RootWerks/gef-dem-verifier/actions)
[![z/OS CEX Gate](https://img.shields.io/badge/hardware-CEX%2FXCF-blueviolet.svg)](https://github.com/RootWerks/gef-dem-verifier)

Deterministic pre-silicon invariant verification and hardware-gated enforcement module for GEF/DEM. Replaces probabilistic AI drift with byte-zero hard stops (`0xF505`/`0xF003`) and 139-byte SMF cryptographic tombstones.

---

## Immediate Verification

    git clone https://github.com/RootWerks/gef-dem-verifier.git
    cd gef-dem-verifier
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python eval.py --vector tests/vectors/drift_epistemic_0xf003.json --verify-smf

---

## Core Architectural Invariant

$$\text{Valid}(\delta \le \delta_{\max}) \land \text{WitnessValid}(F_{\text{token}}, R(t)) \land \neg\text{CatProhibited}(A_{\text{semantic}})$$

| Invariant Term | Symbol | Enforcement Target | Disposition / Gate Action |
| :--- | :--- | :--- | :--- |
| **Drift Bound** | $\delta \le \delta_{\max}$ | Epoch State $R(t)$ | Abort on threshold breach (`0xF003`) |
| **Token Witness** | $F_{\text{token}}$ | Cryptographic Binding | ICSF / CEX root-hash verification |
| **Semantic Check** | $\neg\text{CatProhibited}$ | Payload Action $A_{\text{semantic}}$ | Byte-zero short-circuit drop (`0xF505`) |

---

## Operational Profile

* **Pre-Silicon CI/CD**: GitHub Actions evaluation harness (`eval.py`) validating multi-vector expectations (`expect_pass`).
* **Hardware Gate**: CEX/ICSF coprocessor intercepts execution prior to RRS Two-Phase Commit (`2PC PREPARE`).
* **Dispositions**: Hard-stop `0xF003` (epistemic/sync drift) or `0xF505` (statutory prohibition).
* **Forensic Ledger**: SMF 0x03/0x05 binary cryptographic tombstones with SHA-256 state-root stamps.

*Cloud-native AI governance polices autonomous loops with sidecars, async telemetry, and hope. Big iron polices them with silicon hard stops.*

**We believe in "Think".**

Deterministic pre-silicon invariant verification and hardware-gated enforcement module.

## Core Architectural Invariant
$$\text{Valid}(\delta \le \delta_{\text{max}}) \land \text{WitnessValid}(E_{\text{token}}, R(t)) \land \neg \text{CatProhibited}(A_{\text{semantic}})$$

## Operational Profile
* **Pre-Silicon CI/CD**: GitHub Actions evaluation harness (`eval.py`) validating multi-vector expectations (`expect_pass`).
* **Hardware Gate**: CEX/ICSF coprocessor intercepts execution prior to RRS Two-Phase Commit (`2PC PREPARE`).
* **Dispositions**: Hard-stop `0xF003` (epistemic/sync drift) or `0xF505` (statutory prohibition).
* **Forensic Ledger**: SMF 0x03/0x05 binary cryptographic tombstones with SHA-256 state-root stamps ($R_{\text{iss}}, R_{\text{prep}}, \delta_{\text{root}}$).

*Cloud-native AI governance polices autonomous loops with sidecars, async telemetry, and hope. Big iron polices them with physics.*

**We believe in "Think".**
