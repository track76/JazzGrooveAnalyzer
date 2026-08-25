#!/usr/bin/env python3
"""Apply the frozen CED-VAL-006 robustness scorer to Phase-1 B/C reports."""

from __future__ import annotations

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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    scorer = load_frozen_scorer()
    scorer.REPORTS = {
        "B_run_1": HERE / "canonical_report_B_run_1.json",
        "B_run_2": HERE / "canonical_report_B_run_2.json",
        "C_run_1": HERE / "canonical_report_C_run_1.json",
        "C_run_2": HERE / "canonical_report_C_run_2.json",
    }
    result = scorer.score()
    result.pop("scoring_fingerprint")
    result["execution_id"] = "EXEC-CEDVAL006-BASS-PRESERVATION-PHASE1-01"
    result["preregistration_id"] = "H-CEDVAL006-BASS-PRESERVATION-PHASE1-01"
    result["preregistration_fingerprint"] = "b6d497595f07a3a68472a39419a18579b28ba3501188e04c8ac90d27da6711f8"
    result["scoring_method_authority"] = {
        "source": str(BASE_SCORER.relative_to(HERE.parents[2])),
        "sha256": sha256(BASE_SCORER.read_bytes()).hexdigest(),
        "status": "EXACT_FROZEN_LEVEL_1_LEVEL_2_LEVEL_3_METHOD_REUSED",
    }
    result["scoring_fingerprint"] = sha256(scorer.canonical(result)).hexdigest()
    args.output.write_bytes(scorer.canonical(result) + b"\n")
    print(result["scoring_fingerprint"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
