#!/usr/bin/env python3
"""Apply the frozen CED-VAL-006 robustness scorer to Phase-2 reports."""

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
        f"M{model}_run_{run}": HERE / f"canonical_report_M{model}_run_{run}.json"
        for model in range(1, 4) for run in range(1, 3)
    }
    result = scorer.score()
    result.pop("scoring_fingerprint")
    result["execution_id"] = "EXEC-CEDVAL006-BASS-PRESERVATION-PHASE2-01"
    result["preregistration_id"] = "H-CEDVAL006-BASS-PRESERVATION-PHASE2-01"
    result["preregistration_fingerprint"] = "8c17046b5b0ef8ea4bc6a88e3b2334e56b07b3ffaff9b5fea7a8b42d0acc1f48"
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
