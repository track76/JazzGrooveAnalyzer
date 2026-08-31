#!/usr/bin/env python3
"""Apply the frozen CED-VAL-006 Level-1/2/3 scorer to remediated Phase 3."""

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_SCORER = HERE.parent / "separation_robustness_20260825_01/score.py"

def load_frozen_scorer():
    spec = importlib.util.spec_from_file_location("frozen_robustness_scorer", BASE_SCORER)
    if spec is None or spec.loader is None:
        raise RuntimeError("frozen scorer unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    scorer = load_frozen_scorer()
    scorer.REPORTS = {f"run_{run}": HERE / f"canonical_report_run_{run}.json" for run in (1, 2)}
    result = scorer.score()
    result.pop("scoring_fingerprint")
    result["execution_id"] = "EXEC-CEDVAL006-BASS-PRESERVATION-PHASE3-REMEDIATED-01"
    result["preregistration_id"] = "H-CEDVAL006-BASS-PRESERVATION-PHASE3-DYNAMICS-01"
    result["preregistration_fingerprint"] = "17f7d3ea16de1cb2aefdd117290970b5b4057f27ec7d9f6c5dc5e5f8b06947a0"
    result["remediation_id"] = "PR-CEDVAL006-PHASE3-DETERMINISTIC-WAV-SERIALIZATION-01"
    result["remediation_result_fingerprint"] = "44eeedd466541d2b4228fe2f8897a288dad8277ca4d71902ad66fc238e48effa"
    result["scoring_method_authority"] = {"source": str(BASE_SCORER.relative_to(HERE.parents[2])), "sha256": sha256(BASE_SCORER.read_bytes()).hexdigest(), "status": "EXACT_FROZEN_LEVEL_1_LEVEL_2_LEVEL_3_METHOD_REUSED"}
    result["scoring_fingerprint"] = sha256(scorer.canonical(result)).hexdigest()
    args.output.write_bytes(scorer.canonical(result) + b"\n")
    print(result["scoring_fingerprint"])

if __name__ == "__main__":
    main()
