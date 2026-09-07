"""Mixture-to-report orchestration with explicit output and preparation provenance."""
from jga.audio.file_audio_source import FileAudioSource
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.reporting.rhythm_section_timing_report import AuthorizedSourceInput
from jga.reporting.rhythm_section_timing_report_service import RhythmSectionTimingReportService
from jga.separation.authorized_demucs import output_audio
from jga.separation.demucs_separator import DemucsSeparator


class DemucsTimingReportService:
    def build(self, mixture, runner, output_directory, *, roles, **report_authority):
        audio = FileAudioSource().load(str(mixture.path),
            source_authority_id=mixture.source_authority_id,
            source_instance_key=mixture.source_instance_key,
            expected_sha256=mixture.expected_sha256)
        stems = DemucsSeparator(runner=runner).separate_authorized(audio, output_directory)
        contexts, sources = {}, []
        by_key = {s.name: s for s in stems}
        for key, role in roles.items():
            stem = by_key[key]
            context = AnalysisPipeline().analyze_audio(output_audio(stem))
            contexts[role['label']] = context
            sources.append(AuthorizedSourceInput(context.audio.path, role['label'],
                role['role'], expected_sha256=stem.asset_sha256,
                separation_provenance=context.audio.transformation_provenance))
        report = RhythmSectionTimingReportService().build(tuple(sources),
            _contexts=contexts, **report_authority)
        return report, stems, contexts
