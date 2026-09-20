# GEF-DEM Verifier (z/OS Silicon Sovereignty)
Deterministic pre-silicon invariant verification and hardware-gated enforcement module.

## Core Architectural Invariant
$\text{Valid}(\delta \le \delta_{\text{max}}) \land \text{WitnessValid}(E_{\text{token}}, R(t)) \land \neg \text{CatProhibited}(A_{\text{semantic}})$

## Operational Profile
* **Pre-Silicon CI/CD**: GitHub Actions evaluation harness (`eval.py`) validating multi-vector expectations (`expect_pass`).
* **Hardware Gate**: CEX/ICSF coprocessor intercepts execution prior to RRS Two-Phase Commit (`2PC PREPARE`).
* **Dispositions**: Hard-stop `0xF003` (epistemic/sync drift) or `0xF505` (statutory prohibition).
* **Forensic Ledger**: SMF 0x03/0x05 binary cryptographic tombstones with SHA-256 state-root stamps ($R_{\text{iss}}, R_{\text{prep}}, \delta_{\text{root}}$).
