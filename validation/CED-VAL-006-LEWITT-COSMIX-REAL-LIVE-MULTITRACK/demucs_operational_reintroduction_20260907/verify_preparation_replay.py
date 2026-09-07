"""Bounded same-asset preparation/observation invariance, not a separation experiment."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from uuid import UUID

from jga.audio.file_audio_source import FileAudioSource
from jga.engines.source_pulse_candidate_builder import SourcePulseCandidateBuilder
from jga.runtime.analysis_context import AnalysisContext
from jga.separation.null_separator import NullSeparator

HERE=Path(__file__).resolve().parent
BASELINE='c7b9b65362303ff17c48897c4d26a518595fe9c5'


def main():
    path='src/jga/engines/source_pulse_candidate_builder.py'
    old_detector=subprocess.check_output(['git','show',BASELINE+':'+path])
    assert old_detector==Path(path).read_bytes()
    old_preparation=subprocess.check_output(['git','show',BASELINE+':src/jga/engines/audio_preprocessor.py'])
    namespace={};exec(compile(old_preparation,'frozen_historical_preprocessor','exec'),namespace)
    report=json.loads((HERE/'canonical_run_1.json').read_text());results={}
    for source in report['source_authorities']:
        audio=FileAudioSource().load(source['path_used'])
        assert audio.asset_sha256==source['sha256']
        audio.source_identity=UUID(source['source_identity'])
        context=AnalysisContext(audio=audio)
        namespace['AudioPreprocessor']().process(context)
        digest=sha256(context.processed_audio.astype('<f4').tobytes()).hexdigest()
        assert digest==source['separation_provenance']['detector_preparation']['prepared_signal_sha256']
        NullSeparator().process(context)
        SourcePulseCandidateBuilder().process(context)
        candidates=context.source_pulse_sequences[0].pulse_candidates
        expected=sorted(report['observations'][source['label']],key=lambda r:r['observation_index'])
        assert [(c.time,c.strength,c.confidence) for c in candidates]==[(r['timestamp_seconds'],r['strength'],r['confidence']) for r in expected]
        results[source['label']]={'count':len(candidates),'prepared_signal_sha256':digest,'timestamp_strength_confidence_exact':True}
    result={'status':'PASS','method':'same WAV -> frozen historical preparation -> unchanged detector; compare new report observations. Historical reports did not serialize strength/confidence.','historical_preparation_source_sha256':sha256(old_preparation).hexdigest(),'unchanged_detector_source_sha256':sha256(old_detector).hexdigest(),'sources':results}
    (HERE/'preparation_replay.json').write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
