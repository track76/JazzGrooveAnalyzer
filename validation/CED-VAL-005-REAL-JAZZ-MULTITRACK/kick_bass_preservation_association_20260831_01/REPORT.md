# Kick/Bass preservation association

Protocol `H-CROSSDATASET-KICK-BASS-PRESERVATION-ASSOCIATION-01`, fingerprint `064e956a27be8ddf3f452d45033abf04b8f143e38d074c672c4feff15add5a22`.

## Primary CED-VAL-005 result

The preregistered negative-association hypothesis was not supported. Bass observations within 30 ms of a KickIn observation were more, not less, likely to be preserved by the frozen htdemucs_ft to JGA pipeline.

- KickIn JGA EME: 475.
- Original BassDI EME: 1,138.
- BASS_WITH_KICK: 170; recovered 139; missed 31; preservation 0.8176470588235294; Wilson 95% CI [0.7528004280867323, 0.868455288085063].
- BASS_WITHOUT_KICK: 968; recovered 643; missed 325; preservation 0.6642561983471075; Wilson 95% CI [0.6339090146374446, 0.6933048504572648].
- Absolute difference P(with)-P(without): +0.15339086047642192; Newcombe 95% CI [+0.08233518014520941, +0.21257217272784623].
- Relative risk: 1.23092123319001; 95% CI [1.1318188682859425, 1.3387010278531803]; relative difference +23.09212331900099%.
- Odds ratio: 2.266342246525862; 95% CI [1.5017744240644988, 3.4201589107415065].
- Phi: +0.11793243007136398.
- Two-sided Fisher exact p: 0.00004881528058733429.

Descriptive bands: 0–10 ms 29/34 recovered (0.85294); >10–30 ms 110/136 (0.80882); >30–60 ms 60/137 (0.43796); >60 ms 583/831 (0.70156). The non-monotonic 30–60 ms result cautions against interpreting the binary result as a physical masking curve.

Temporal-quarter preservation remained higher with Kick in all four quarters. Mantel-Haenszel OR across temporal quarters was 2.286373680701728. Density-stratified Mantel-Haenszel OR was 2.2886869293327594. The fixed adjusted logistic model converged and estimated Kick OR 2.2302803546596244, Wald 95% CI [1.4628472181488745, 3.4003212356483], controlling normalized time, local Bass count, and local Kick count within +/-0.5 s.

## Secondary CED-VAL-006 result

The isolated close dynamic Kick capsule yielded 676 JGA EME. The evidence is analogous but not acquisition-identical to CED-VAL-005 KickIn.

- BASS_WITH_KICK: 573; recovered 392; missed 181; preservation 0.6841186736474695.
- BASS_WITHOUT_KICK: 482; recovered 227; missed 255; preservation 0.470954356846473.
- Absolute difference: +0.21316431680099646; Newcombe 95% CI [+0.1537865154026117, +0.27059945721894024].
- Relative risk: 1.4526220295069616; relative difference +45.262202950696164%.
- Odds ratio: 2.4328863144060167; Fisher p 2.7229841324750015e-12; phi +0.21563873106258274.
- Temporal-quarter MH OR 2.4263658358586926; density MH OR 2.3788015625647656; adjusted Kick OR 2.447813066825212, 95% CI [1.8496347953656869, 3.239444254148358].

## Authority and interpretation

KickIn was selected prospectively as the sole CED-VAL-005 Kick authority because it is the isolated in-drum attack-oriented close microphone. KickOut was excluded before outcome linkage and was not used as a sensitivity-driven substitute or union. CED-VAL-006 used its prospectively selected isolated close dynamic Kick capsule; generic Drum EME were not substituted.

This is an association between source-labelled JGA observations. It does not show that Kick physically improves recovery. Plausible uncontrolled common causes include event strength, ensemble emphasis, metric position, Bass articulation, detector salience, microphone bleed, and separator behavior. Local count and coarse temporal controls do not remove these confounds. JGA EME are observations rather than physical-onset Ground Truth, and the two Kick microphones are analogous rather than identical acquisition authorities.

The preregistered substantial negative association gate failed because the observed risk difference was positive. Therefore the conditional harmonic-evidence next experiment is not recommended from this result.

Replay: both Kick observation populations replayed byte-identically; both analysis executions replayed byte-identically. Result fingerprint `49b8145b406d20da08cc669e94989fe0c9ca68de79d993401b2dcd30b4c4fb1f`.
