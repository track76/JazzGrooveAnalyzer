"""Validate complete neutral AD-037 timing representation."""

from __future__ import annotations

import hashlib
import json
import statistics
from decimal import Decimal
from pathlib import Path

from jga.domain.declared_metric_reference import DeclaredMetricReference, MetricReferenceProvenance
from jga.domain.declared_metric_timeline import DeclaredAnalysisScope, DeclaredQuarterPhaseOrigin
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
SCOPE_END = Decimal(1865728) / Decimal(44100)
PERIOD = Decimal(10) / Decimal(13)
MUSICXML_SHA256 = "809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778"
SOURCES = (
    ("Drums", "drums.wav", "d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd", 63),
    ("Piano", "piano.wav", "26fa1158f375598cc7c01e04379c00547ef1787f6862eb2f29a36aafd9007c7e", 49),
    ("Double Bass", "double_bass.wav", "31d6f2e34d360c6f8f75362187433f2a2c1f5eb5cbbfe627305e99d07d8be6c5", 27),
    ("Tenor Sax", "tenor_sax.wav", "89dd7e5c6063d3c4d5e4ac59c9119c265df4257dfb1b4a1e01b5f117ee87182e", 16),
)

def sha256(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical(value): return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()

def analyze(label, filename, checksum, expected):
    path = ROOT / "recordings/validation/stems" / filename
    if sha256(path) != checksum: raise RuntimeError(f"asset mismatch: {label}")
    tempo_prov = MetricReferenceProvenance("GT-VAL-001-v1", "authoritative controlled-source MusicXML", MUSICXML_SHA256, "complete controlled performance")
    asset_prov = MetricReferenceProvenance(f"CED-VAL-001-{filename}", "authoritative controlled audio asset", checksum, "complete controlled performance")
    context = AnalysisPipeline().analyze(
        str(path),
        declared_metric_reference=DeclaredMetricReference(Decimal("78"), "quarter", tempo_prov),
        declared_quarter_phase_origin=DeclaredQuarterPhaseOrigin(Decimal("0"), asset_prov),
        declared_analysis_scope=DeclaredAnalysisScope(Decimal("0"), SCOPE_END, checksum, asset_prov),
    )
    events = {event.id: event for event in context.elementary_metric_events}
    candidates = {candidate.id: candidate for candidate in context.domain_pulse_candidates}
    beats = {beat.id: beat for beat in context.beat_references}
    rows = []
    for association in context.elementary_metric_event_associations:
        event = events[association.elementary_metric_event_id]
        preceding = beats[association.beat_reference_id]
        following = beats.get(association.following_beat_reference_id)
        exact_event = Decimal(round(event.timestamp * 44100 / 512)) * Decimal(512) / Decimal(44100)
        elapsed = exact_event - preceding.exact_timestamp_seconds
        phase = elapsed / PERIOD
        if following is not None:
            next_delta = exact_event - following.exact_timestamp_seconds
            nearest = elapsed if abs(elapsed) <= abs(next_delta) else next_delta
            nearest_id = preceding.id if abs(elapsed) <= abs(next_delta) else following.id
        else:
            nearest, nearest_id = elapsed, preceding.id
        support = [candidates[item] for item in event.supporting_pulse_candidate_ids]
        rows.append({
            "eme_id": str(event.id), "timestamp_seconds": str(exact_event),
            "contributor_id": str(event.contributor_id), "sound_source_id": str(event.sound_source_id),
            "preceding_beat_reference_id": str(preceding.id), "preceding_index": preceding.index,
            "following_beat_reference_id": str(following.id) if following else None,
            "following_index": following.index if following else None,
            "elapsed_from_preceding_seconds": str(elapsed), "normalized_phase": str(phase),
            "nearest_beat_reference_id": str(nearest_id), "signed_nearest_displacement_seconds": str(nearest),
            "supporting_pulse_candidates": [{"id": str(c.id), "observation_index": c.observation_index,
                "observation_provenance_id": c.observation_provenance_id, "strength": c.strength} for c in support],
            "timeline": {"origin_seconds": "0", "period_seconds": "10/13", "scope_end_seconds": str(SCOPE_END),
                         "tempo_status": "DECLARED", "phase_origin_status": "DECLARED", "asset_sha256": checksum},
        })
    if len(rows) != expected or len(events) != expected or len(context.beat_references) != 55:
        raise RuntimeError(f"cardinality mismatch: {label}")
    phases = [Decimal(row["normalized_phase"]) for row in rows]
    offsets = [Decimal(row["signed_nearest_displacement_seconds"]) for row in rows]
    strengths = [Decimal(str(row["supporting_pulse_candidates"][0]["strength"])) for row in rows]
    return {"count": len(rows), "events": rows, "summary": {
        "normalized_phase_range": [str(min(phases)), str(max(phases))],
        "median_normalized_phase": str(statistics.median(phases)),
        "signed_displacement_range_seconds": [str(min(offsets)), str(max(offsets))],
        "median_signed_displacement_seconds": str(statistics.median(offsets)),
        "strength_range": [str(min(strengths)), str(max(strengths))],
    }}

def execute():
    contributors = {label: analyze(label, filename, checksum, count) for label, filename, checksum, count in SOURCES}
    total = sum(item["count"] for item in contributors.values())
    result = {"experiment_id": "H-VAL001-EME-NEUTRAL-01", "status": "PASS", "contributors": contributors,
              "total_eme": total, "represented_eme": total, "metric_losses": 0, "metric_merges": 0,
              "metric_creations": 0, "beat_reference_count_per_analysis": 55, "voice_status": "DEFERRED",
              "musical_interpretation_performed": False, "production_correction_performed": False}
    result["scientific_fingerprint"] = hashlib.sha256(canonical(result)).hexdigest()
    return result

first, second = execute(), execute()
if canonical(first) != canonical(second): raise RuntimeError("deterministic replay failure")
(RUN / "result.json").write_bytes(canonical(first) + b"\n")
