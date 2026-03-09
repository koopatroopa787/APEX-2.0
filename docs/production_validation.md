# Production Readiness Validation Framework

## Overview
63.7% of enterprise LLM tools stall in "Pilot Purgatory." To win the "Real-World Impact" criteria, the APEX platform integrates an actuarial validation process directly into its deployment CI/CD.

## Mechanics (`agents/production_readiness`)

1. **Validators (`validators.py`)**: Assesses current telemetry against 10 isolated heuristics (DB Throttling Limits, Cost Thresholds, Security Identity Scopes, P95 SLAs).
2. **Cox Proportional Hazards (`survival_models.py`)**: Uses the `lifelines` statistical technique to determine the empirical probability that the agentic infrastructure will "survive" the next 30 or 90 days. Models failure rates derived from simulated synthetic chaos data.
3. **Risk Scorer (`risk_scoring.py`)**: Fuses the heuristics (70% weight) and the hazard prediction (30% weight) to create a final 0-100 percentage.
4. **Agent 7 (`agent.py`)**: Packages the scoring into a deterministic Go/No-Go CI/CD gate.

## Running the Simulation

Execute the localized stress test:
```bash
python scripts/production_simulation.py
```
This forces a simulated workload, generating realistic `mock_telemetry_post_simulation` to demonstrate the validation engine's recommendations in action.
