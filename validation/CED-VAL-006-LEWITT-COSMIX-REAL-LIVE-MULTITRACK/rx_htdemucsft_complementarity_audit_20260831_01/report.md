# RX11 versus htdemucs_ft Complementarity Audit

- Audit: `AUD-CEDVAL006-RX-HTDEMUCSFT-COMPLEMENTARITY-01`
- Protocol fingerprint: `5d5718e6be95e3ac5db63f37dd4744bc5d5085983b09848d670d373b79c950a8`
- Classification: `LIMITED_COMPLEMENTARITY`
- Future non-Ground-Truth consensus/fusion study: `YES`

## Exhaustive original-event partition

| Population | Count | Percent of 1,055 |
|---|---:|---:|
| Both | 555 | 52.6066% |
| htdemucs_ft only | 64 | 6.0664% |
| RX only | 38 | 3.6019% |
| Neither | 398 | 37.7251% |

The recovered-original union is 657 events (recall 0.6227488151658768),
including 38 events beyond the stronger individual separator. Intersection
recall is 0.5260663507109005 and recovered-set Jaccard overlap is
0.8447488584474886. RX recovers 38/436 (0.0871559633027523) Demucs-missed
events; Demucs recovers 64/462 (0.13852813852813853) RX-missed events.

Within the 555 shared events, RX is closer to the original comparison time for
324, htdemucs_ft for 229, with 2 ties. Nevertheless, aggregate shared-event
absolute localization favors htdemucs_ft: median/RMSE 0.00645805/0.01601036 s
versus RX 0.01066667/0.01795753 s. The RX-minus-Demucs absolute-displacement
difference has median -0.00116100 s and RMSE 0.01421541 s, documenting a
heterogeneous event-level comparison rather than an oracle selection rule.

Demucs-only events have absolute-displacement median/RMSE/max
0.01237188/0.02955886/0.13612698 s. RX-only events have
0.01066667/0.04245562/0.13866667 s.

The evidence supports prospectively studying separator agreement together
with detector-native confidence or consistency as Ground-Truth-independent
evidence for consensus or abstention. It does not authorize selecting the
separator closest to the original Bass authority.
