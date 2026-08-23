"""Execute frozen PulseCandidate strength measurement-authority study."""

from hashlib import sha256
import json
import platform
from pathlib import Path
from statistics import fmean, median, pstdev
import sys

import numpy as np

from jga.engines.pulse_candidate_builder import PulseCandidateBuilder
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline


BASE = Path("validation/CED-VAL-003-SWING-3-4")
RUN = BASE / "run_20260823_211259"
POPULATION = BASE / "preregistrations/frozen_ambiguous_population.json"
PREREG = BASE / "preregistrations/H-CEDVAL003-PULSECANDIDATE-STRENGTH-AUTHORITY-01.md"
EXTERNAL = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-003-SWING")
SOURCES = {
    "Drums": EXTERNAL / "steams/CED-VAL-003-SWING-3-4_drums.wav",
    "Double Bass": EXTERNAL / "steams/CED-VAL-003-SWING-3-4_bass.wav",
}
EXPECTED = {
    str(POPULATION): "7544282135cae86f13076f1eb70d35c2feb82dacd36ae849bc4b08fa3c4f5ac8",
    str(PREREG): "a64866681d5095be04c501e93ceea8e8d2af0b988c4408446c74399cd9848600",
    str(BASE / "input_authority_manifest.json"): "f53ce38c5324981753310736e47dd2620364e9a1a71848af50b4d5fb35d5e085",
    str(BASE / "run_20260823_205731/audit_result.json"): "5da81ca50b072c4af332acf8e403c1d1c520e86af8378ba6125fabd764ce4af4",
    str(BASE / "preregistrations/EG-CEDVAL003-AMBIGUOUS-PHYSICAL-AUTHORITY-01.md"): "77885fcd2d1a83e5f32335c9d814541275884af39fe094fbde8f812a5f2a0a08",
    str(SOURCES["Drums"]): "11bd51037126608d7052ae0bb2b01d77b86eccae46d60ca088d3d5f57cccc44d",
    str(SOURCES["Double Bass"]): "bd702128f0b6e9887ccfae104ee0af6b2b4307c2021bb826fd85fec669322429",
    "src/jga/engines/pulse_candidate_builder.py": "788c13ac7e108860907b3031ea056569e45b7531b1e92993f3895224c114ff59",
    "src/jga/engines/pulse_candidate_filter.py": "a0982865cb09d8df1b5e108cdf8b53371ccb69dc9ff713175ea0ab5be9439f44",
    "src/jga/engines/source_pulse_candidate_builder.py": "5b270f352483dde91448b0958a299c08e51d064ab867bc872ef1cdde37a81c32",
    "src/jga/engines/domain_pulse_candidate_adapter.py": "6a3d276bf50534bc6823075a26787c624ab7a8d2ecca58628579fb86658a9330",
    "src/jga/domain/services/elementary_metric_event_builder.py": "137e390a69c9361d5cbfd66908256b2417d76c95d503e7ad2c409cd2e1b66cc2",
    "src/jga/pipeline/default_analysis_pipeline.py": "04ecdfee536717b977276b91b7e9416701e7a89ce9aa7bc4339917263725ef17",
}
ASSET_SHA = {
    "Drums": EXPECTED[str(SOURCES["Drums"])],
    "Double Bass": EXPECTED[str(SOURCES["Double Bass"])],
}
HOP = 512
SAMPLE_RATE = 44100


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def descriptive(values: tuple[float, ...]) -> dict:
    if not values:
        return {key: None for key in ("minimum", "maximum", "mean", "median", "population_standard_deviation", "q1", "q2", "q3")} | {"n": 0}
    quartiles = np.quantile(np.asarray(values), (0.25, 0.5, 0.75), method="linear")
    return {
        "n": len(values), "minimum": min(values), "maximum": max(values),
        "mean": fmean(values), "median": median(values),
        "population_standard_deviation": pstdev(values),
        "q1": float(quartiles[0]), "q2": float(quartiles[1]), "q3": float(quartiles[2]),
    }


def analyze_once(population: dict) -> list[dict]:
    contexts = {source: AnalysisPipeline().analyze(str(path)) for source, path in SOURCES.items()}
    records = []
    for cell in population["cells"]:
        source = cell["source"]
        if source == "Piano":
            raise RuntimeError("Unexpected Piano ambiguous cell")
        context = contexts[source]
        emes = {str(item.id): item for item in context.elementary_metric_events}
        candidates = {str(item.id): item for item in context.domain_pulse_candidates}
        if len(emes) != len(context.elementary_metric_events) or len(candidates) != len(context.domain_pulse_candidates):
            raise RuntimeError(f"Duplicate reproduced identity: {source}")
        for frozen in cell["observations"]:
            eme = emes.get(frozen["eme_id"])
            if eme is None:
                raise RuntimeError(f"Missing EME join: {frozen['eme_id']}")
            frozen_ids = frozen["supporting_pulse_candidate_ids"]
            if len(frozen_ids) != 1 or tuple(str(item) for item in eme.supporting_pulse_candidate_ids) != tuple(frozen_ids):
                raise RuntimeError(f"Non-unique EME lineage: {frozen['eme_id']}")
            candidate = candidates.get(frozen_ids[0])
            if candidate is None:
                raise RuntimeError(f"Missing PulseCandidate join: {frozen_ids[0]}")
            if eme.timestamp.hex() != float(frozen["timestamp_seconds"]).hex() or candidate.timestamp.hex() != eme.timestamp.hex():
                raise RuntimeError(f"Exact timestamp mismatch: {frozen['eme_id']}")
            if eme.source_asset_sha256 != ASSET_SHA[source] or eme.sound_source_id != candidate.sound_source_id:
                raise RuntimeError(f"Provenance mismatch: {frozen['eme_id']}")
            frame = round(candidate.timestamp * SAMPLE_RATE / HOP)
            if candidate.timestamp.hex() != float(frame * HOP / SAMPLE_RATE).hex():
                raise RuntimeError(f"Frame-authority mismatch: {frozen['eme_id']}")
            records.append({
                "cell_identity": cell["cell_identity"], "cell_index": cell["cell_index"],
                "source": source, "eme_id": str(eme.id), "pulse_candidate_id": str(candidate.id),
                "observation_index": candidate.observation_index, "observation_frame": frame,
                "timestamp": candidate.timestamp, "timestamp_hex": candidate.timestamp.hex(),
                "strength": candidate.strength, "strength_hex": candidate.strength.hex(),
                "confidence": candidate.confidence, "confidence_hex": candidate.confidence.hex(),
                "contributor_id": str(eme.contributor_id), "sound_source_id": str(candidate.sound_source_id),
                "asset_sha256": eme.source_asset_sha256, "temporal_scope": eme.temporal_scope,
                "observation_provenance_id": candidate.observation_provenance_id,
                "materialization_rule": eme.materialization_rule,
                "observation_configuration": "AnalysisPipeline;librosa-onset;hop=512;sr=44100;unchanged",
                "replay_status": "PENDING_SECOND_EXECUTION",
            })
    return sorted(records, key=lambda item: (item["source"], item["cell_index"], item["eme_id"]))


def main() -> None:
    for name, expected in EXPECTED.items():
        if checksum(Path(name)) != expected:
            raise RuntimeError(f"Input checksum mismatch: {name}")
    population = json.loads(POPULATION.read_text(encoding="utf-8"))
    first = analyze_once(population)
    second = analyze_once(population)
    if canonical(first) != canonical(second):
        raise RuntimeError("Exact deterministic replay mismatch")
    if len(first) != 112:
        raise RuntimeError("Recovered population mismatch")
    for record in first:
        record["replay_status"] = "EXACT_MATCH"
    summaries = {
        source: descriptive(tuple(record["strength"] for record in first if record["source"] == source))
        for source in ("Drums", "Double Bass", "Piano")
    }
    scientific = {
        "study_id": "H-CEDVAL003-PULSECANDIDATE-STRENGTH-AUTHORITY-01",
        "dataset_fingerprint": "9345f5923055a7ed1c953eee4b8613f2b2262c55cd2e5f094d489d097c37f790",
        "population_manifest_sha256": EXPECTED[str(POPULATION)],
        "records": first, "descriptive_strength_by_source": summaries,
        "population": {"cells": 56, "observations": 112, "Drums": 108, "Double Bass": 4, "Piano": 0},
        "lineage_join_failures": 0, "deterministic_replay": True,
        "exact_value_reproducibility": True, "ground_truth_accessed": False,
        "selection_or_ranking_performed": False, "cross_source_comparability_authorized": False,
        "within_source_measurement_authority": True, "discrimination_authority": False,
        "historical_h02_scores_changed": False, "h02_changed": False, "h03_created": False,
        "calibration_zero_changed": False, "raw_observations_changed": False,
        "production_code_changed": False,
    }
    fingerprint = sha256(canonical(scientific)).hexdigest()
    result = {"status": "PASS", "scientific_fingerprint": fingerprint, "scientific_content": scientific}
    (RUN / "strength_measurements.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {
        "preregistration_commit": "ce8b93e", "preregistration_sha256": EXPECTED[str(PREREG)],
        "frozen_inputs": EXPECTED, "python": sys.version, "platform": platform.platform(),
        "numpy": np.__version__, "hop_samples": PulseCandidateBuilder.FRAME_LENGTH_SAMPLES,
        "sample_rate_hz": SAMPLE_RATE, "symbolic_authority_opened": False,
        "h02_scoring_opened": False,
    }
    (RUN / "input_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "counts": scientific["population"], "statistics": summaries, "fingerprint": fingerprint}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
