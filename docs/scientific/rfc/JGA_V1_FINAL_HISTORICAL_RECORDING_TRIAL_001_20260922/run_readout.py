"""Serialization-only compatibility adapter; frozen analysis rules unchanged."""
import json
import runpy
import sys
from pathlib import Path
import numpy as np

original = json.JSONEncoder.default
def numpy_scalar(self, value):
    if isinstance(value, np.generic):
        return value.item()
    return original(self, value)

json.JSONEncoder.default = numpy_scalar
sys.argv = ['trial.py', 'analyze']
runpy.run_path(str(Path(__file__).with_name('trial.py')), run_name='__main__')
