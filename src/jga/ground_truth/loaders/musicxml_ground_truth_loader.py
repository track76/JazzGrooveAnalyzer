"""MusicXML loader for the approved M83 Ground Truth reference."""

from decimal import Decimal
from hashlib import sha256
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
    """Loads only the approved GT-VAL-001-v1 MusicXML reference."""

    GROUND_TRUTH_ID = "GT-VAL-001-v1"
    VALIDATION_DATASET_ID = "VAL-001"
    SCHEMA_VERSION = "1"
    NORMALIZATION_VERSION = "1"
    SOURCE_PATH = (
        "recordings/validation/ground_truth/"
        "03 THE COST OF LIVING versione intro + 8 bar.musicxml"
    )
    SOURCE_SHA256 = (
        "809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778"
    )

    _INSTRUMENT_CATEGORIES = {
        ("Voce", "Voice (2)"): "Voice",
        ("Sax Tenore", "Tenor Saxophone (2)"): "Saxophone",
        ("Piano", "Piano (2)"): "Piano",
        ("Basso Verticale", "Upright Bass"): "Double Bass",
        ("Set di batteria", "Drum Set (Jazz)"): "Drum Set",
    }

    def load(
        self,
        source: Path,
        repository_revision: str | None = None,
    ) -> GroundTruth:
        source_bytes = source.read_bytes()
        checksum = sha256(source_bytes).hexdigest()

        if source.as_posix() != self.SOURCE_PATH:
            raise ValueError("MusicXML source is not the approved M83 source.")
        if checksum != self.SOURCE_SHA256:
            raise ValueError("MusicXML source checksum does not match AD-028.")

        root = ElementTree.fromstring(source_bytes)
        time_signature = self._read_time_signature(root)
        tempo = self._read_tempo(root)
        measures = self._read_measure_mapping(root)
        instruments = self._read_instruments(root)

        return GroundTruth(
            ground_truth_id=self.GROUND_TRUTH_ID,
            validation_dataset_id=self.VALIDATION_DATASET_ID,
            provenance=GroundTruthProvenance(
                schema_version=self.SCHEMA_VERSION,
                normalization_version=self.NORMALIZATION_VERSION,
                source=AuthoritativeSourceProvenance(
                    repository_path=self.SOURCE_PATH,
                    sha256=checksum,
                    repository_revision=repository_revision,
                ),
            ),
            time_signature=time_signature,
            tempo=tempo,
            measures=measures,
            sections=(
                GroundTruthSection(
                    name="Intro",
                    start_full_measure=1,
                    measure_count=4,
                ),
                GroundTruthSection(
                    name="A",
                    start_full_measure=5,
                    measure_count=8,
                ),
            ),
            instruments=instruments,
        )

    @staticmethod
    def _read_time_signature(root: ElementTree.Element) -> GroundTruthTimeSignature:
        time = root.find("./part/measure/attributes/time")
        if time is None:
            raise ValueError("MusicXML source has no initial time signature.")

        beats = time.findtext("beats")
        beat_type = time.findtext("beat-type")
        if beats is None or beat_type is None:
            raise ValueError("MusicXML time signature is incomplete.")

        return GroundTruthTimeSignature(
            beats=int(beats),
            beat_type=int(beat_type),
        )

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
    ) -> tuple[GroundTruthMeasure, ...]:
        first_part = root.find("./part")
        if first_part is None:
            raise ValueError("MusicXML source has no score parts.")

        source_ids = tuple(
            measure.attrib["number"] for measure in first_part.findall("measure")
        )
        expected_ids = tuple(str(number) for number in range(1, 14))
        if source_ids != expected_ids:
            raise ValueError("MusicXML measure sequence does not match AD-028.")

        return tuple(
            GroundTruthMeasure(
                source_measure_id=source_id,
                normalized_full_measure=None if source_id == "1" else int(source_id) - 1,
                is_pickup=source_id == "1",
            )
            for source_id in source_ids
        )

    def _read_instruments(
        self,
        root: ElementTree.Element,
    ) -> tuple[GroundTruthInstrument, ...]:
        instruments: list[GroundTruthInstrument] = []

        for score_part in root.findall("./part-list/score-part"):
            part_id = score_part.attrib.get("id")
            part_name = score_part.findtext("part-name")
            instrument_name = score_part.findtext("score-instrument/instrument-name")
            if part_id is None or part_name is None or instrument_name is None:
                raise ValueError("MusicXML instrument designation is incomplete.")

            designation = (part_name, instrument_name)
            try:
                category = self._INSTRUMENT_CATEGORIES[designation]
            except KeyError as error:
                raise ValueError(
                    "MusicXML instrument designation is not approved by AD-028."
                ) from error

            instruments.append(
                GroundTruthInstrument(
                    source_part_id=part_id,
                    source_part_name=part_name,
                    source_instrument_name=instrument_name,
                    canonical_category=category,
                )
            )

        return tuple(instruments)
