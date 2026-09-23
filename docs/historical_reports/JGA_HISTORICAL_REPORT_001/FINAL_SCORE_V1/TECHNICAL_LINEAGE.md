# Exact reporting conventions and lineage

Source and parent: ../REPORT_FREEZE.json and ../SUMMARY.json. Full-mix asset SHA-256 aec97cfb67096bd6a7c3d432f025523d1269b6b261e2dd6bc01a33c045acac45. Analysis [0,330); existing ending excluded. All native/source/quarter assignments reused from ../data. PRIMARY_NONSHARED and DISTINCT_PAIR unchanged. ORIGINAL_PAIRS.csv preserves the existing P01–P21 byte stream; the extended table only adds metric fields/aliases, retaining coordinates, signed differences and annotation state. Original source states remain untouched.

Metric: zero-based index i>=2 has beat=(i−2)%4+1, measure=floor((i−2)/4)+1. Q=i+1. Pre-anchor Q1–Q2 are retained without invented measure/beat labels. Last measure incomplete. Propagation is PI-authorized indexing, not a new downbeat detector or an independent validation of every downbeat.

Tempo: every consecutive 32-interval window from i=2 through i=872 inclusive uses references i...i+32 (33 references); BPM=1920/(t[i+32]−t[i]); curve x=(first+last)/2. Start Q3–Q35, 0.8126984126984127–12.49233560090703 s. End Q873–Q905, 318.02049886621313–329.7233560090703 s. No window exceeds [0,330), no averaging reciprocal BPM, no smoothing. Joined observations aid reading only. Central remains frozen median over 904 raw intervals, not redefined by the curve.

Row local BPM: for a row starting at zero-based reference s, use the 32-interval window beginning max(2,min(s−8,872)); this centers an eight-measure window on a full four-measure row's index midpoint, clamping at available boundaries. Exact window IDs recorded per row. This is a deterministic display convention, not a new estimator. Time-based x coordinates preserve native positions and unequal PLP intervals. Four-measure rows retain midpoint cell outer boundaries; the initial row also displays Q1–Q2 as pre-anchor context. Final row contains only remaining measures.

Color selects source-conditioned PRIMARY_NONSHARED observations having exclusive original Bass/Drum state. All Dual stays gray square even where it supplies a qualified primary/pair hypothesis. No Dual is reclassified or duplicated. All 1606 native observations appear once across pages; original global selections remain preserved in parent evidence. Shape/color constants reuse the frozen format. Values rounded only for display; exact values remain CSV/JSON. No ON tolerance. Sample-coordinate comparison identifies tied pair extremes without retiming decimal inputs.

Historical whole-performance overview remains in parent Report 001 figures. This package is additive. JGA v1 detection/identity/hybrid architecture and historical scientific results are unchanged.

FUTURE_NON_SPECIALIST_EXPLANATORY_PAGE: deferred, not designed here. Future human form workflow may accept arbitrary lengths/irregular structure; not implemented.
