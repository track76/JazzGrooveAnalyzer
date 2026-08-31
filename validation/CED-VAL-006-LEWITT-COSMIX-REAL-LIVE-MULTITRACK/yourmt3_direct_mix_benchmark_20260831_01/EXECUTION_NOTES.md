# Execution notes

- Benchmark: `CED-VAL-006-YOURMT3-DIRECT-MIX-BASS-BENCHMARK-20260831-01`
- Protocol fingerprint: `8794858b0569a80ac62751be8bd07ce7e3a7164ff87d1fbe68133e72e21e6b1f`
- Preregistration commit: `00c7a31`
- Runner correction commit: `f833f3a`
- First two runner invocations produced no result file: both stopped on the mechanical complementarity key mismatch `B_DEMUCS_ONLY`. The protocol and matching method were unchanged. The runner key was corrected from `B_HTDEMUCS_FT_ONLY` to the authority's actual key `B_DEMUCS_ONLY`.
- Completed execution 1 wall/user/sys: `0.38 / 0.28 / 0.04 s`.
- Completed execution 2 wall/user/sys: `0.34 / 0.29 / 0.02 s`.
- `execution_1.json` SHA-256: `101fae489f4f8114857744674d0e54ff8c58db433d3b7f080457e568d7d25e12`.
- `execution_2.json` SHA-256: `101fae489f4f8114857744674d0e54ff8c58db433d3b7f080457e568d7d25e12`.
- Byte comparison: PASS (`cmp` exit 0).
- Result fingerprint: `ff34eda3b4f0ec3811da8495388fc6ede99cee67ad0abefe667fc69140f5583d`.
- YourMT3 inference was not rerun.
- JGA and every frozen authority remained read-only.
- Push was not performed.
