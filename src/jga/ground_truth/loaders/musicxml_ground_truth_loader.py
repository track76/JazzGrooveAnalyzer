"""Data-defined MusicXML Ground Truth loader."""

from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
from xml.etree import ElementTree

from jga.ground_truth.loaders.ground_truth_loader import GroundTruthLoader
from jga.ground_truth.models import (
    AuthoritativeSourceProvenance,
    GroundTruth,
    GroundTruthInstrument,
    GroundTruthMeasure,
    GroundTruthProvenance,
    GroundTruthSection,
    GroundTruthTempo,
    GroundTruthTimeSignature,
)


class MusicXmlGroundTruthLoader(GroundTruthLoader):
    """Load immutable Ground Truth using repository data beside MusicXML."""

    DEFINITION_SUFFIX = ".ground_truth.json"

    def __init__(
        self,
        repository_root: Path = Path("."),
        definition_path: Path | None = None,
    ) -> None:
        self.repository_root = repository_root
        self.definition_path = definition_path

    def load(
        self,
        source: Path,
        repository_revision: str | None = None,
    ) -> GroundTruth:
        source_path = self._repository_path(source)
        definition_path = self.definition_path or source_path.with_suffix(
            self.DEFINITION_SUFFIX
        )
        definition = json.loads(
            (self.repository_root / definition_path).read_text(encoding="utf-8")
        )
        source_definition = definition["source"]
        source_bytes = (self.repository_root / source_path).read_bytes()
        checksum = sha256(source_bytes).hexdigest()

        if source_path.as_posix() != source_definition["repository_path"]:
            raise ValueError(
                "MusicXML source identity does not match Ground Truth data."
            )
        if checksum != source_definition["sha256"]:
            raise ValueError(
                "MusicXML source checksum does not match Ground Truth data."
            )
        if (
            repository_revision is not None
            and repository_revision != source_definition["repository_revision"]
        ):
            raise ValueError(
                "MusicXML source revision does not match Ground Truth data."
            )

        root = ElementTree.fromstring(source_bytes)
        measures = self._read_measure_mapping(root, definition["measures"])
        instruments = self._read_instruments(
            root,
            definition["instrument_normalization"],
        )

        return GroundTruth(
            ground_truth_id=definition["ground_truth_id"],
            validation_item_id=definition["validation_item_id"],
            provenance=GroundTruthProvenance(
                schema_version=definition["schema_version"],
                normalization_version=definition["normalization_version"],
                source=AuthoritativeSourceProvenance(
                    repository_path=source_definition["repository_path"],
                    sha256=checksum,
                    repository_revision=source_definition["repository_revision"],
                ),
            ),
            time_signature=self._read_time_signature(root),
            tempo=self._read_tempo(root),
            measures=measures,
            sections=tuple(
                GroundTruthSection(
                    name=section["name"],
                    start_full_measure=section["start_full_measure"],
                    measure_count=section["measure_count"],
                )
                for section in definition["sections"]
            ),
            instruments=instruments,
        )

    def _repository_path(self, source: Path) -> Path:
        if source.is_absolute():
            try:
                return source.relative_to(self.repository_root.resolve())
            except ValueError as error:
                raise ValueError(
                    "MusicXML source is outside the repository."
                ) from error
        return source

    @staticmethod
    def _read_time_signature(root: ElementTree.Element) -> GroundTruthTimeSignature:
        time = root.find("./part/measure/attributes/time")
        if time is None:
            raise ValueError("MusicXML source has no initial time signature.")

        beats = time.findtext("beats")
        beat_type = time.findtext("beat-type")
        if beats is None or beat_type is None:
            raise ValueError("MusicXML time signature is incomplete.")

        return GroundTruthTimeSignature(beats=int(beats), beat_type=int(beat_type))

    @staticmethod
    def _read_tempo(root: ElementTree.Element) -> GroundTruthTempo:
        metronome = root.find("./part/measure/direction/direction-type/metronome")
        if metronome is None:
            raise ValueError("MusicXML source has no initial metronome indication.")

        beat_unit = metronome.findtext("beat-unit")
        per_minute = metronome.findtext("per-minute")
        if beat_unit is None or per_minute is None:
            raise ValueError("MusicXML metronome indication is incomplete.")

        return GroundTruthTempo(
            beats_per_minute=Decimal(per_minute),
            beat_unit=beat_unit,
        )

    @staticmethod
    def _read_measure_mapping(
        root: ElementTree.Element,
        definitions: list[dict[str, object]],
    ) -> tuple[GroundTruthMeasure, ...]:
        first_part = root.find("./part")
        if first_part is None:
            raise ValueError("MusicXML source has no score parts.")

        source_ids = tuple(
            measure.attrib["number"] for measure in first_part.findall("measure")
        )
        defined_ids = tuple(item["source_measure_id"] for item in definitions)
        if source_ids != defined_ids:
            raise ValueError(
                "MusicXML measure sequence does not match Ground Truth data."
            )

        return tuple(
            GroundTruthMeasure(
                source_measure_id=item["source_measure_id"],
                normalized_full_measure=item["normalized_full_measure"],
                is_pickup=item["is_pickup"],
            )
            for item in definitions
        )

    @staticmethod
    def _read_instruments(
        root: ElementTree.Element,
        definitions: list[dict[str, str]],
    ) -> tuple[GroundTruthInstrument, ...]:
        categories = {
            (item["source_part_name"], item["source_instrument_name"]): item[
                "canonical_category"
            ]
            for item in definitions
        }
        instruments: list[GroundTruthInstrument] = []

        for score_part in root.findall("./part-list/score-part"):
            part_id = score_part.attrib.get("id")
            part_name = score_part.findtext("part-name")
            instrument_name = score_part.findtext("score-instrument/instrument-name")
            if part_id is None or part_name is None or instrument_name is None:
                raise ValueError("MusicXML instrument designation is incomplete.")

            designation = (part_name, instrument_name)
            try:
                category = categories[designation]
            except KeyError as error:
                raise ValueError(
                    "MusicXML instrument designation is absent from Ground Truth data."
                ) from error

            instruments.append(
                GroundTruthInstrument(
                    source_part_id=part_id,
                    source_part_name=part_name,
                    source_instrument_name=instrument_name,
                    canonical_category=category,
                )
            )

        if len(instruments) != len(definitions):
            raise ValueError(
                "Ground Truth instrument normalization does not match MusicXML parts."
            )
        return tuple(instruments)
