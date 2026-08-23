"""Mechanically freeze accepted ambiguous-cell membership without GT timing."""

from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/CED-VAL-003-SWING-3-4")
SOURCE = BASE / "run_20260823_203324/event_level_results.json"
OUTPUT = BASE / "preregistrations/frozen_ambiguous_population.json"
EXPECTED_SHA = "3c2d22300de63de57885a1c786dea1679136410860558f3e093e6bf2b5233c31"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if digest(SOURCE) != EXPECTED_SHA:
        raise RuntimeError("Calibration Zero event authority checksum mismatch")
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    cells = []
    for contributor in ("Drums", "Double Bass", "Piano"):
        records = source["correspondence_by_source"][contributor]["event_results"]
        for record in records:
            if record["correspondence_status"] != "AMBIGUOUS_MULTIPLE_OBSERVED":
                continue
            observations = []
            for candidate in record["candidate_emes"]:
                observations.append(
                    {
                        "eme_id": candidate["eme_id"],
                        "supporting_pulse_candidate_ids": candidate[
                            "supporting_pulse_candidate_ids"
                        ],
                        "timestamp_seconds": candidate["t_jga_seconds"]["decimal"],
                    }
                )
            cells.append(
                {
                    "cell_identity": f"CEDVAL003:{contributor}:{record['cell_index']}",
                    "cell_index": record["cell_index"],
                    "source": contributor,
                    "observations": observations,
                }
            )
    counts = {
        contributor: {
            "cells": sum(cell["source"] == contributor for cell in cells),
            "observations": sum(
                len(cell["observations"])
                for cell in cells
                if cell["source"] == contributor
            ),
        }
        for contributor in ("Drums", "Double Bass", "Piano")
    }
    if counts != {
        "Drums": {"cells": 54, "observations": 108},
        "Double Bass": {"cells": 2, "observations": 4},
        "Piano": {"cells": 0, "observations": 0},
    } or len(cells) != 56:
        raise RuntimeError("Frozen ambiguous population mismatch")
    payload = {
        "schema": "JGA-AMBIGUOUS-STRENGTH-POPULATION/v1",
        "authority": "AUD-CEDVAL003-H02-SCORABILITY-01",
        "calibration_event_authority_sha256": EXPECTED_SHA,
        "counts": counts,
        "cells": cells,
        "ground_truth_timestamps_included": False,
        "scoring_outcomes_included": False,
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(digest(OUTPUT))


if __name__ == "__main__":
    main()
