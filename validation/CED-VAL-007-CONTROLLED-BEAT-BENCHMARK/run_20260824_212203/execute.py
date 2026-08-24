"""Execute frozen H-CEDVAL007-THREE-SYSTEM-SYMBOLIC-BEAT-RECOVERY-01."""
from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BASE = Path("validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK")
RUN = BASE / "run_20260824_212203"
EXECUTION_ID = "EXEC-CEDVAL007-THREE-SYSTEM-BENCHMARK-20260824-212203"
STUDY_ID = "H-CEDVAL007-THREE-SYSTEM-SYMBOLIC-BEAT-RECOVERY-01"
PREREG_COMMIT = "4126d7992150629a1cfb7294cda10dab1df11ee7"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fraction_field(record: dict, name: str) -> Fraction:
    return Fraction(record[name]["exact"])


def winners(scores: dict, metric: str, maximize: bool) -> list[str]:
    values = {system: fraction_field(score, metric) for system, score in scores.items()}
    target = (max if maximize else min)(values.values())
    return [system for system in ("JGA", "LIBROSA", "ESSENTIA") if values[system] == target]


def decimal_winners(scores: dict, path: tuple[str, ...], minimize: bool = True) -> list[str]:
    values = {}
    for system, score in scores.items():
        value = score
        for key in path:
            value = value[key]
        values[system] = Decimal(value)
    target = (min if minimize else max)(values.values())
    return [system for system in ("JGA", "LIBROSA", "ESSENTIA") if values[system] == target]


def main(use_existing_frozen_outputs: bool = False) -> None:
    RUN.mkdir(parents=True, exist_ok=True)
    if not use_existing_frozen_outputs:
        subprocess.run([sys.executable, str(RUN / "freeze_outputs.py"), str(RUN)], check=True, cwd=Path.cwd(), env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"})
    elif not all((RUN / name).is_file() for name in ("jga_raw_output.json", "librosa_raw_output.json", "essentia_raw_output.json", "shared_mono_authority.json", "raw_system_output_authority.json")):
        raise RuntimeError("FROZEN_RAW_OUTPUT_AUTHORITY_MISSING")
    # Ground Truth is first opened by these scoring subprocesses, after raw authority freeze.
    with tempfile.TemporaryDirectory(prefix="cedval007-three-system-scoring-") as temp_name:
        temp = Path(temp_name)
        first = temp / "score_pass_1.json"
        second = temp / "score_pass_2.json"
        command = [sys.executable, str(RUN / "score.py"), str(RUN)]
        subprocess.run(command + [str(first)], check=True, cwd=Path.cwd(), env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"})
        subprocess.run(command + [str(second)], check=True, cwd=Path.cwd(), env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"})
        if first.read_bytes() != second.read_bytes():
            raise RuntimeError("SCORING_REPLAY_CONFLICT")
        shutil.copyfile(first, RUN / "scientific_content.json")
    scientific = json.loads((RUN / "scientific_content.json").read_text())
    scores = scientific["systems"]
    comparison = {
        "highest_precision": winners(scores, "precision", True),
        "highest_recall": winners(scores, "recall", True),
        "highest_f1": winners(scores, "f1", True),
        "lowest_median_absolute_error": decimal_winners(scores, ("absolute_error_statistics", "milliseconds", "median_linear", "decimal")),
        "lowest_rmse": decimal_winners(scores, ("absolute_error_statistics", "milliseconds", "rmse")),
    }
    comparison["metric_winners_identical_across_all_criteria"] = len({tuple(value) for value in comparison.values()}) == 1
    raw_authority = json.loads((RUN / "raw_system_output_authority.json").read_text())
    mono = json.loads((RUN / "shared_mono_authority.json").read_text())
    input_manifest = {
        "execution_id": EXECUTION_ID,
        "study_id": STUDY_ID,
        "preregistration_commit": PREREG_COMMIT,
        "dataset_authority": "PR-CED-VAL-007-CONTROLLED-BEAT-BENCHMARK-001",
        "dataset_fingerprint": "cd93455778d1484067f9a3caa3037b6467d27c7e8d5a8c0df694658bad2484e9",
        "input_sha256": "c673d2c104eb3eb31012154f1bd84ee81313b4fd36b61bf3913686f43e19bb0c",
        "ground_truth_authority": "SYMBOLIC_BEAT_GROUND_TRUTH",
        "ground_truth_sha256": "c2035145967dc436e08210d57a8ecdbe0ad39c309d253a06cb3c700a99405431",
        "shared_mono_raw_bytes_sha256": mono["raw_bytes_sha256"],
        "raw_system_output_authority_fingerprint": raw_authority["combined_raw_output_fingerprint"],
    }
    result = {
        "execution_id": EXECUTION_ID,
        "study_id": STUDY_ID,
        "status": scientific["status"],
        "combined_benchmark_fingerprint": scientific["combined_benchmark_fingerprint"],
        "deterministic_raw_output_replay": raw_authority["replay"],
        "deterministic_scoring_replay": "PASS_EXACT_TWO_INDEPENDENT_EXECUTIONS",
        "system_results": {system: {key: scores[system][key] for key in ("raw_output_count", "matched_count", "missed_gt_count", "extra_output_count", "precision", "recall", "f1", "exact_zero_match_count", "scientific_fingerprint")} for system in scores},
        "comparison": comparison,
        "firewalls": scientific["firewalls"],
    }
    write_json(RUN / "input_manifest.json", input_manifest)
    write_json(RUN / "result.json", result)
    write_json(RUN / "completion_protocol.json", {"execution_id": EXECUTION_ID, "status": result["status"], "raw_output_freeze_before_ground_truth": "PASS", "system_replay": raw_authority["replay"], "scoring_replay": result["deterministic_scoring_replay"], "combined_benchmark_fingerprint": result["combined_benchmark_fingerprint"]})
    rows = []
    for system in ("JGA", "LIBROSA", "ESSENTIA"):
        score = scores[system]
        rows.append(f"| {system} | {score['raw_output_count']} | {score['matched_count']} | {score['missed_gt_count']} | {score['extra_output_count']} | {score['precision']['decimal']} | {score['recall']['decimal']} | {score['f1']['decimal']} | {score['absolute_error_statistics']['milliseconds']['median_linear']['decimal']} | {score['absolute_error_statistics']['milliseconds']['rmse']} |")
    (RUN / "report.md").write_text(
        f"# {EXECUTION_ID}\n\nStatus: **{result['status']}**\n\nCombined fingerprint: `{result['combined_benchmark_fingerprint']}`.\n\n"
        "| System | Raw | Matched | Missed | Extra | Precision | Recall | F1 | Median abs ms | RMSE ms |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n" + "\n".join(rows) + "\n\n"
        "JGA is reported as the ability of its Drums observational population to recover the controlled symbolic beat schedule, not as beat-tracker accuracy. JGA and librosa are not fully algorithmically independent; Essentia is the more independent comparator. No universal-superiority claim or latency correction is authorized.\n"
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main(use_existing_frozen_outputs="--use-existing-frozen-outputs" in sys.argv[1:])
