# JGA-QUARTER-NEAREST-ONSET-GROOVE-001

STATUS: **PASS** for procedure, assignment, preservation and additive delivery. Scientific decision **B. SUPPORTED WITH QUALIFICATION**. Track: PI-designated Ray Brown Trio — Exactly Like You. No canonical behavior change.

## Authority, preregistration and measurement

Parent integrity PASS: source audio,1627 existing native events,946 frozen quarters,states,timestamps,whole-track and trajectory-validation freezes verify. This preregistration SHA-256 `2ed3d1d7a8c064f61ed24c1e8a04292c6494cacdf8c2f4f766f2eff8fe61c71e` preceded selection and all new groove summaries. Full authority chain in PARENT_INTEGRITY.json. Original whole-track procedure/result and trajectory-validation result remain unchanged.

Quarter cells use exact Decimal stored coordinates. Interior cells(L,R] give exact midpoint ownership to the earlier quarter; first[0,R],last(L,acoustic_end). The acoustic end remains342.6568707482993 s, with terminal digital zeros excluded. No extrapolated quarter. Winner minimizes absolute native-marker distance within its own cell, ties earlier event thenID. Source state never enters selection. No borrowing across cells.

QUARTER_NEAREST_ONSET_OFFSET_MS=(original native timestamp−frozen owning quarter timestamp)*1000. Negative before,positive after,zero exact. This is a new quarter-indexed representation of native markers, not attack-time refinement. No unwrapping or event-cycle association was computed.

## Assignment and coverage

946/946 cells;898 quarters selected;48 EMPTY;coverage94.9260%. Event reuse0,ties0. All1627 events accounted for exactly once:898 PRIMARY plus729 CONTEXT. Independent brute-force nearest-quarter and nearest-event recomputation passed; timestamps,source states,quarter references,BPM and original offset values preserved. All52 primary window boundaries retained.

257 UNKNOWN primary selections remain emphasized. In186 cases a farther source-supported context event exists; it did not replace the nearer UNKNOWN. This verifies the intended source-neutral selection behavior.

## Whole-track primary offsets

N898;448 negative,0 exact zero,450 positive. Range−182.82 to+182.43 ms;median+0.17 ms;Q1−45.32,Q3+53.45,IQR98.77 ms. Median absolute distance49.73 ms;absolute IQR70.24 ms. Absolute P25/P75=20.85/91.08 ms,P90=129.82,P95=152.11,P99=173.03 ms. Full signed/absolute quantiles in WHOLE_TRACK_QUARTER_STATISTICS.csv.

Descriptive cumulative distance counts(denominator898 selected markers; these are not validity thresholds):

|Absolute distance|N|Selected percentage|
|---|---:|---:|
|<= 5 ms|63|7.02%|
|<= 10 ms|117|13.03%|
|<= 20 ms|222|24.72%|
|<= 35 ms|350|38.98%|
|<= 50 ms|450|50.11%|
|<= 75 ms|589|65.59%|
|<= 100 ms|699|77.84%|
|> 100 ms|199|22.16%|

## Primary source composition

|Frozen source state|SelectedN|Selected%|All-eventN|All-event%|
|---|---:|---:|---:|---:|
|DRUM_SUPPORTED|513|57.13%|898|55.19%|
|BASS_SUPPORTED|6|0.67%|9|0.55%|
|BASS_AND_DRUM_SUPPORTED|122|13.59%|198|12.17%|
|CONFLICTING_EVIDENCE|0|0.00%|0|0.00%|
|UNKNOWN|257|28.62%|522|32.08%|

Composition differences are descriptive selection effects, not causal enrichment or improved identity accuracy. Context composition is also preserved in PRIMARY_SOURCE_COMPOSITION.csv.

## Quarter-indexed variation and fixed windows

Of945 adjacent-quarter pairs,866 have both selected markers;79 differences remain unavailable because a quarter is EMPTY. Absolute adjacent change:median29.60 ms,IQR76.90 ms,range0.0173–354.07 ms.267 valid adjacent pairs switch offset sign;391 switch provisional source state. These do not imply continuation of one physical source.

Across52 unchanged complete windows,selected-offset medians range−121.15 to+90.21 ms,median−5.86,IQR41.70. Half-shifts range−201.17 to+184.09 ms,median+1.37,IQR71.92;25 negative and27 positive. Time slopes range−41.88 to+25.49 ms/s,median−0.30,IQR15.62;27 negative and25 positive. Quarter-index slopes are separately retained in WINDOW_RESULTS.csv. No unwrapping or continuous event-strand claim follows from these descriptive slopes.

Window membership is based on frozen quarter timestamps. A selected event outside a reporting window can still represent a quarter inside it; such cases are explicitly counted. Empty quarters remain in window coverage and BPM summaries.

## Reference122–128.5 s

17 quarters,17 selected,0 empty. Source composition5 Drum,1 Bass,11 dual,0 UNKNOWN/conflicts. Median−13.26 ms,IQR41.77;first-half median−4.00 ms(N8),second-half−45.37 ms(N9);half-shift **−41.38 ms**;time slope **−11.14 ms/s**;index slope−4.06 ms/quarter.

The previous all-event reference remains−50.24 ms half-shift and−11.64 ms/s slope. The new representation answers a different question and is not required to agree.

Chronological reference selections(original quarter IDs retained; printed times rounded only):

|QuarterID|Quarter time(s)|NativeID|Native time(s)|Offset(ms)|Frozen state|
|---|---:|---|---:|---:|---|
|332|122.337929|F_MIX_00602|122.334331|-3.60|BASS_AND_DRUM_SUPPORTED|
|333|122.702681|F_MIX_00603|122.705850|+3.17|BASS_AND_DRUM_SUPPORTED|
|334|123.067411|F_MIX_00604|123.054150|-13.26|BASS_AND_DRUM_SUPPORTED|
|335|123.432121|F_MIX_00606|123.425669|-6.45|BASS_AND_DRUM_SUPPORTED|
|336|123.796814|F_MIX_00608|123.797188|+0.37|BASS_AND_DRUM_SUPPORTED|
|337|124.161492|F_MIX_00610|124.157098|-4.39|BASS_AND_DRUM_SUPPORTED|
|338|124.525692|F_MIX_00612|124.528617|+2.92|BASS_AND_DRUM_SUPPORTED|
|339|124.889463|F_MIX_00613|124.876916|-12.55|BASS_AND_DRUM_SUPPORTED|
|340|125.253560|F_MIX_00615|125.236825|-16.73|BASS_AND_DRUM_SUPPORTED|
|341|125.618663|F_MIX_00616|125.585125|-33.54|BASS_AND_DRUM_SUPPORTED|
|342|125.983958|F_MIX_00618|125.991474|+7.52|BASS_SUPPORTED|
|343|126.350315|F_MIX_00620|126.304943|-45.37|BASS_AND_DRUM_SUPPORTED|
|344|126.716740|F_MIX_00622|126.699683|-17.06|DRUM_SUPPORTED|
|345|127.082513|F_MIX_00624|127.024762|-57.75|DRUM_SUPPORTED|
|346|127.447699|F_MIX_00626|127.396281|-51.42|DRUM_SUPPORTED|
|347|127.812358|F_MIX_00628|127.744580|-67.78|DRUM_SUPPORTED|
|348|128.176542|F_MIX_00630|128.127710|-48.83|DRUM_SUPPORTED|

## Previous recurrence intervals, unchanged boundaries

|Window|Seconds|Quarters / selected / empty|Median ms|First → second median ms|Half-shift ms|Slope ms/s|
|---|---|---:|---:|---:|---:|---:|
|W011|65.302–71.802|17 / 17 / 0|-19.56|2.61 → -87.03|-89.64|-28.27|
|W012|71.802–78.302|17 / 17 / 0|7.61|77.65 → -52.63|-130.28|-41.88|
|W038|240.802–247.302|18 / 17 / 1|-27.96|17.31 → -45.83|-63.14|-7.84|

All three have negative quarter-nearest half-shifts/slopes, with different medians,dispersion and magnitudes. This is descriptive similarity in the new representation, not rescue of the previous unwrapped-trajectory claim or proof of a common musical mechanism.

## BPM relationship

Selected-quarter Spearman N898:stored BPM↔signed offset rho+0.009;BPM↔absolute distance−0.007. Across52 windows,median BPM↔median selected offset−0.041;median absolute distance−0.035;half-shift−0.038;time slope+0.271. These do not support reduction of this geometry to stored BPM alone; they do not prove statistical independence or absence of nonlinear relationships.

## Secondary UNKNOWN-excluded sensitivity

Remove selected UNKNOWN only, never replace with a farther marker:641 selections remain. Median−4.90 ms,IQR106.44;median absolute distance52.37 ms,absolute IQR71.67. The257 removed UNKNOWN selections remain PRIMARY in the actual result; original48 EMPTY quarters remain separately identified. Whole-track and all window sensitivity summaries are in SOURCE_SENSITIVITY.csv.

## Figures and context preservation

Whole-track figure draws all946 quarter references,898 primary markers,729 light-gray context markers and48 empty-quarter indicators. UNKNOWN uses a dark primary triangle. Dual uses one purple marker. No offset-dependent hiding. Original native timestamps supply marker x-coordinates; each marker's signed offset uses its owning frozen quarter.

Detailed figure marks exact122/128.5 bounds and includes neighboring cells for edge context:19 quarter cells,19 selected markers and15 context events are displayed, while the reference statistics contain only the17 quarters whose timestamps fall inside the requested interval. Neighboring extra markers are not added to the reference statistics. Rounded figure labels such as+0 ms do not imply an exact zero offset.

## Concept test and scientific interpretation

- deterministic_one_per_nonempty_quarter: **YES**.
- removes_mixed_source_unwrapping_requirement: **YES**.
- full_event_context_preserved: **YES**.
- measurable_quarter_indexed_variation: **YES-WITH-QUALIFICATION**.
- reducible_to_stored_BPM_alone: **NO-NOT-SUPPORTED**.

The frozen internal pulse defines the quarter sequence. For each quarter,JGA identifies the nearest observable native event as the primary local groove marker. Other events remain visible as contextual rhythmic information. The succession of quarter-indexed local configurations provides a groove description without requiring a unique continuous mixed-source event trajectory.

The representation is supported with qualification:empty quarters,candidate availability,UNKNOWN identity and existing pulse-reference limitations remain scientifically material. It does not become canonical production behavior.

## Limitations and next action

- Selected events are nearest observable native markers, not the true beat, physical on-beat attacks or performer intentions.
- Nearest selection mechanically favors small distances and depends on candidate coverage/density; smaller offsets are not evidence of more accurate timing.
- 48 EMPTY quarters mean no native candidate in that cell, not instrumental silence.257 primary markers retain UNKNOWN identity.
- Quarter grid is numerically continuous but independent whole-track pulse/metrical qualification remains limited; the new representation does not validate or refit it.
- Continuous mixed-source trajectory remains NOT ESTABLISHED / INSUFFICIENT. Quarter-indexed comparisons need no source-stream continuity, but jumps between selected events may reflect changed identity/subdivision or nearest-event competition.
- Dual support remains one marker with two identity hypotheses. No independent physical Bass-versus-Drum microtiming or full-mix Bass attack measurement is established.
- The52 windows are unchanged, but membership here is by quarter timestamp. The reference overlaps some comparison windows and is not independent replication of them.
- Rank associations do not establish causality, independence, absence of nonlinear relationships or universal musical generalization.
- Noncanonical additive pilot only; no production architecture/runtime change.

ONE recommendation only: **Preregister a bounded candidate-coverage sensitivity audit of the quarter-nearest representation.** Not executed. Preserve the prior trajectory-validation decision D — INSUFFICIENT; this pilot avoids that requirement rather than solving mixed-stream continuity.

Source/freeze and assignment integrity PASS. Documentation synchronization follows this additive result freeze and has its own manifest/recovery audit. No inference,canonical data/code change,staging,commit or push. STOP for PI review.
