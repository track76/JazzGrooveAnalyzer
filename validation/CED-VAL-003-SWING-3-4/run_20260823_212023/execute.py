"""Execute frozen exact within-cell strength discriminability study."""

from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
from statistics import fmean, median, pstdev

import numpy as np


BASE = Path("validation/CED-VAL-003-SWING-3-4")
RUN = BASE / "run_20260823_212023"
INPUT = BASE / "run_20260823_211259/strength_measurements.json"
INPUT_ARTIFACT_MANIFEST = BASE / "run_20260823_211259/artifact_manifest.json"
PREREG = BASE / "preregistrations/H-CEDVAL003-WITHIN-CELL-STRENGTH-DISCRIMINABILITY-01.md"
EXPECTED = {
    str(INPUT): "1772b2817b0a6aa075b91cff20b830791c14f245a5c219d6a65feee7f19450cc",
    str(INPUT_ARTIFACT_MANIFEST): "c30f7b2a0ea77e3205f8cfaa6868906f19c438fef48dde7a162daf88dbc5e008",
    str(PREREG): "e0499331bca210e52e22f977297f519e8bc630091369f70fcb19c279c656649d",
}
INPUT_FINGERPRINT = "6903decbe3175db300002f148d5e4192f9c51ba8959a6534921675af753aa94d"


def checksum(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def descriptive(values: tuple[float, ...]) -> dict:
    if not values:
        return {key: None for key in ("minimum", "maximum", "mean", "median", "population_standard_deviation", "q1", "q2", "q3")} | {"n": 0, "sorted_values": []}
    quartiles = np.quantile(np.asarray(values), (0.25, 0.5, 0.75), method="linear")
    return {
        "n": len(values), "minimum": min(values), "maximum": max(values),
        "mean": fmean(values), "median": median(values),
        "population_standard_deviation": pstdev(values),
        "q1": float(quartiles[0]), "q2": float(quartiles[1]), "q3": float(quartiles[2]),
        "sorted_values": sorted(values),
    }


def transform(records: list[dict]) -> dict:
    by_cell = defaultdict(list)
    for record in records:
        if float.fromhex(record["strength_hex"]) != record["strength"]:
            raise RuntimeError(f"Strength round-trip failure: {record['pulse_candidate_id']}")
        if record["replay_status"] != "EXACT_MATCH":
            raise RuntimeError(f"Input replay failure: {record['pulse_candidate_id']}")
        by_cell[record["cell_identity"]].append(record)
    if len(by_cell) != 56 or any(len(items) != 2 for items in by_cell.values()):
        raise RuntimeError("Frozen cell population mismatch")
    cells = []
    for cell_identity, items in sorted(by_cell.items()):
        groups = defaultdict(list)
        for item in items:
            groups[item["strength_hex"]].append(item)
        ordered_strengths = sorted(
            groups,
            key=lambda strength_hex: float.fromhex(strength_hex),
            reverse=True,
        )
        order_groups = []
        for strength_hex in ordered_strengths:
            group_items = sorted(groups[strength_hex], key=lambda item: item["pulse_candidate_id"])
            order_groups.append({
                "strength": float.fromhex(strength_hex), "strength_hex": strength_hex,
                "observations": [{"eme_id": item["eme_id"], "pulse_candidate_id": item["pulse_candidate_id"]} for item in group_items],
            })
        top = order_groups[0]
        if len(top["observations"]) == 1:
            status = "UNIQUE_STRENGTH_MAXIMUM"
            maximum = top["observations"][0]
            second_strength = order_groups[1]["strength"]
            difference = top["strength"] - second_strength
        else:
            status = "STRENGTH_TIED"
            maximum = None
            difference = 0.0
        source = items[0]["source"]
        if any(item["source"] != source for item in items):
            raise RuntimeError(f"Cross-source cell: {cell_identity}")
        cells.append({
            "cell_identity": cell_identity, "cell_index": items[0]["cell_index"], "source": source,
            "contained_eme_ids": sorted(item["eme_id"] for item in items),
            "contained_pulse_candidate_ids": sorted(item["pulse_candidate_id"] for item in items),
            "strength_order_groups": order_groups, "status": status,
            "unique_maximum_observation": maximum,
            "highest_minus_second_highest_strength": difference,
            "highest_minus_second_highest_strength_hex": difference.hex(),
            "provenance": [{
                key: item[key] for key in (
                    "eme_id", "pulse_candidate_id", "source", "observation_index", "observation_frame",
                    "timestamp", "timestamp_hex", "strength", "strength_hex", "confidence", "confidence_hex",
                    "contributor_id", "sound_source_id", "asset_sha256", "temporal_scope",
                    "observation_provenance_id", "materialization_rule", "observation_configuration",
                )
            } for item in sorted(items, key=lambda item: item["pulse_candidate_id"])],
            "deterministic_replay_status": "PENDING_SECOND_TRANSFORMATION",
        })
    counts = {
        source: {
            "cells": sum(cell["source"] == source for cell in cells),
            "UNIQUE_STRENGTH_MAXIMUM": sum(cell["source"] == source and cell["status"] == "UNIQUE_STRENGTH_MAXIMUM" for cell in cells),
            "STRENGTH_TIED": sum(cell["source"] == source and cell["status"] == "STRENGTH_TIED" for cell in cells),
            "STRENGTH_UNRESOLVED": sum(cell["source"] == source and cell["status"] == "STRENGTH_UNRESOLVED" for cell in cells),
        }
        for source in ("Drums", "Double Bass", "Piano")
    }
    distributions = {
        source: descriptive(tuple(cell["highest_minus_second_highest_strength"] for cell in cells if cell["source"] == source))
        for source in ("Drums", "Double Bass", "Piano")
    }
    return {"cells": cells, "counts_by_source": counts, "difference_distributions_by_source": distributions}


def main() -> None:
    for path, expected in EXPECTED.items():
        if checksum(Path(path)) != expected:
            raise RuntimeError(f"Frozen input checksum mismatch: {path}")
    source = json.loads(INPUT.read_text(encoding="utf-8"))
    if source["scientific_fingerprint"] != INPUT_FINGERPRINT or source["status"] != "PASS":
        raise RuntimeError("Strength measurement authority mismatch")
    scientific_input = source["scientific_content"]
    if scientific_input["ground_truth_accessed"] or scientific_input["selection_or_ranking_performed"]:
        raise RuntimeError("Input firewall mismatch")
    first = transform(scientific_input["records"])
    second = transform(scientific_input["records"])
    if canonical(first) != canonical(second):
        raise RuntimeError("Deterministic transformation replay mismatch")
    for cell in first["cells"]:
        cell["deterministic_replay_status"] = "EXACT_MATCH"
    scientific = {
        "study_id": "H-CEDVAL003-WITHIN-CELL-STRENGTH-DISCRIMINABILITY-01",
        "input_strength_authority_fingerprint": INPUT_FINGERPRINT,
        **first,
        "population": {"cells": 56, "observations": 112, "Drums": 108, "Double Bass": 4, "Piano": 0},
        "exact_binary64_comparison": True, "threshold_or_tolerance_used": False,
        "cross_source_comparison_performed": False, "ground_truth_accessed": False,
        "correspondence_selection_performed": False, "deterministic_replay": True,
        "historical_h02_scores_changed": False, "h02_changed": False, "h03_created": False,
        "calibration_zero_changed": False, "raw_observations_changed": False,
        "architecture_impact": "NONE", "production_impact": "NONE", "production_code_changed": False,
    }
    fingerprint = sha256(canonical(scientific)).hexdigest()
    result = {"status": "PASS", "scientific_fingerprint": fingerprint, "scientific_content": scientific}
    (RUN / "discriminability_result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {"preregistration_commit": "b36ec458a248ae5eb28bfde796b0255f37989fc1", "frozen_inputs": EXPECTED, "ground_truth_accessed": False, "h02_scoring_accessed": False}
    (RUN / "input_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "counts": scientific["counts_by_source"], "distributions": scientific["difference_distributions_by_source"], "fingerprint": fingerprint}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
