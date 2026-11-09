from datetime import datetime,timezone
from uuid import UUID
from jga.domain.pulse_candidate import PulseCandidate
from jga.engines.bass_candidate_attribution_engine import BassCandidateAttributionEngine
from jga.source_understanding.bass_candidate_attribution import BassAttributionDecision,CandidateInputRepresentation
def candidate():return PulseCandidate(UUID(int=1),UUID(int=2),.25,.4,.5,datetime(2000,1,1,tzinfo=timezone.utc),7,'synthetic-fixture')
def test_unknown_default_preserves_identity_and_observation_lineage():
 c=candidate();r=BassCandidateAttributionEngine().attribute([c],CandidateInputRepresentation.FULL_MIX)[0];assert r.decision is BassAttributionDecision.UNKNOWN;assert (r.candidate_id,r.source_id,r.timestamp,r.observation_index,r.observation_provenance_id)==(c.id,c.sound_source_id,c.timestamp,7,'synthetic-fixture')
def test_input_candidate_is_unchanged_by_attribution():
 c=candidate();before=repr(c);BassCandidateAttributionEngine().attribute([c],CandidateInputRepresentation.STEM);assert repr(c)==before
def test_no_candidates_means_no_forced_events():
 assert BassCandidateAttributionEngine().attribute([],CandidateInputRepresentation.FULL_MIX)==()
