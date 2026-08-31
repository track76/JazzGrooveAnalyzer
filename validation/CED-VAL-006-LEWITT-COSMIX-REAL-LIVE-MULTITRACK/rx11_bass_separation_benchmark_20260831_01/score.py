#!/usr/bin/env python3
"""Apply the exact frozen CED-VAL-006 Level-1/2/3 scorer to RX Bass."""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/"separation_robustness_20260825_01/score.py"
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--output",required=True,type=Path); args=parser.parse_args()
    spec=importlib.util.spec_from_file_location("frozen_scorer",BASE); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    module.REPORTS={f"run_{n}":HERE/f"canonical_report_run_{n}.json" for n in (1,2)}
    result=module.score(); result.pop("scoring_fingerprint")
    result["execution_id"]="EXEC-CEDVAL006-RX11-BASS-SEPARATION-BENCHMARK-01"
    result["preregistration_id"]="H-CEDVAL006-RX11-BASS-SEPARATION-BENCHMARK-01-R1"
    result["preregistration_fingerprint"]="6484ebe976e9f9e698e5af18a18e50b4e36c213eac9904f04f2a5ad015a008fe"
    result["rx_output_sha256"]="5588acd3d88e99a8aaca2c762b9a6a9a4fa263cdda03c7a56e2bc9b90b0fa26b"
    result["scoring_method_authority"]={"source":str(BASE.relative_to(HERE.parents[2])),"sha256":sha256(BASE.read_bytes()).hexdigest(),"status":"EXACT_FROZEN_LEVEL_1_LEVEL_2_LEVEL_3_METHOD_REUSED"}
    result["scoring_fingerprint"]=sha256(module.canonical(result)).hexdigest(); args.output.write_bytes(module.canonical(result)+b"\n"); print(result["scoring_fingerprint"])
if __name__=="__main__": main()
