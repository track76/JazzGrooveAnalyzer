# H-VAL001-EME-PHASE-01 — Frozen Result

Status: COMPLETE

Epistemic status: DERIVED EVIDENCE

## Firewall and preservation

The checksum-bound preregistration was executed without symbolic Ground Truth.
Voice remained deferred. All 155 authorized EME entered exactly once; none was
removed, merged or duplicated. No musical or subdivision interpretation was
performed.

## Contributor results

### Drums

- EME: 63; raw phase range: `[0.005551020408, 0.569668934240]`.
- Selected full-sample model: `K=4`.
- Admissible BIC: `K0=231.572510367578`, `K1=235.921875293890`,
  `K2=40.498494831477`, `K3=34.131303546739`, `K4=34.100509421106`.
- `K=5..21` were inadmissible because effective component membership fell
  below three.
- Components `(center, kappa, circular SD, weight, effective membership)`:
  `(0.016082211497, 111.698311633526, 0.015092970522, 0.321460664415,
  20.252021858138)`, `(0.063314035041, 111.698311633526, 0.015092970522,
  0.091237748284, 5.747978141862)`, `(0.515697718898,
  111.698311633526, 0.015092970522, 0.285384774001, 17.979240903124)`,
  `(0.562771752285, 111.698311633526, 0.015092970522, 0.301916813300,
  19.020759096876)`.
- Bootstrap selected-K frequencies: `K2=0.005`, `K3=0.544`, `K4=0.451`.
- Component correspondence frequency: `0.451` each. Complete 95% intervals
  are preserved in `result.json.gz`.
- Stability: `UNSTABLE`; classification: `INSUFFICIENT_EVIDENCE`.

### Piano

- EME: 49; raw phase range: `[0.011827664399, 0.537306122449]`.
- Selected full-sample model: `K=2`.
- Admissible BIC: `K0=180.111952508116`, `K1=182.634958353725`,
  `K2=40.798894889171`.
- `K=3..16` were inadmissible because effective component membership fell
  below three.
- Components: `(0.027283702245, 111.698311633526, 0.015092970522,
  0.591833955815, 28.999863834929)` and `(0.508133117434, 5.317754447242,
  0.072956910314, 0.408166044185, 20.000136165071)`.
- Bootstrap selected-K frequencies: `K2=0.692`, `K3=0.308`.
- Component correspondence frequency: `0.692` each. Complete center, weight
  and concentration 95% intervals are preserved in `result.json.gz`.
- Stability: `UNSTABLE`; classification: `INSUFFICIENT_EVIDENCE`.

### Double Bass

- EME: 27; raw phase range: `[0.015691609977, 0.604680272109]`.
- Selected full-sample model: `K=2`.
- Admissible BIC: `K0=99.245361586105`, `K1=104.045142645778`,
  `K2=1.041952242540`.
- `K=3..9` were inadmissible because effective component membership fell
  below three.
- Component 0: center `0.028797608662` (`95% [0.024205952253,
  0.032798814917]`), kappa `111.698311633526` (`95%
  [111.698311633526,111.698311633526]`), circular SD `0.015092970522`,
  weight `0.407407407407` (`95% [0.222755513238,0.592592592593]`), effective
  membership `11.0`.
- Component 1: center `0.530758861126` (`95% [0.524900918839,
  0.540189089494]`), kappa `70.101808229953` (`95%
  [27.198147876528,111.698311633526]`), circular SD `0.019077406479`,
  weight `0.592592592593` (`95% [0.407407407407,0.777244486762]`), effective
  membership `16.0`.
- Bootstrap selected-K frequencies: `K1=0.0005`, `K2=0.978`, `K3=0.0215`.
- Component correspondence frequency: `0.978` each.
- Stability: `STABLE`; classification: `TWO_STABLE_PHASE_POPULATIONS`.

### Tenor Sax

- EME: 16; raw phase range: `[0.027283446712, 0.572081632653]`.
- Selected full-sample model: `K=2`.
- Admissible BIC: `K0=58.812066125099`, `K1=60.896848675037`,
  `K2=34.674717071308`.
- `K=3..5` were inadmissible because effective component membership fell
  below three.
- Components: `(0.089754434519, 3.449745575338, 0.094484394498,
  0.375186049249, 6.002976784146)` and `(0.549126318330,
  52.526333591152, 0.022066097647, 0.624813950751, 9.997023215854)`.
- Bootstrap selected-K frequencies: `K1=0.0285`, `K2=0.901`, `K3=0.070`,
  `K4=0.0005`.
- Component correspondence frequency: `0.901` each. Complete 95% intervals
  are preserved in `result.json`.
- Stability: `UNSTABLE`; classification: `INSUFFICIENT_EVIDENCE`.

## Structural comparison

Full-sample selections are `K4` for Drums and `K2` for Piano, Double Bass and
Tenor Sax. Only Double Bass satisfies the preregistered 95% stability rule.
Consequently no pair of independently stable contributors exists and the
preregistered shared-center comparison is not authorized. The evidence does
not establish common contributor topology.

## Reproducibility

Independent full-fit replay is identical. Scientific fingerprint:
`75fea68e4e3d6af29241e49a37d9bfd9ec2d0fb1ca822ff02a5466f4a4a1f8c2`.
The complete candidate inventory, rejected-model reasons, 8,000 bootstrap
records, EME identities, timestamps, phases, circular coordinates and
provenance are preserved in `result.json.gz`; the uncompressed raw result is
also preserved under `JGA_EXTERNAL_ROOT` with its checksum in the manifest.
