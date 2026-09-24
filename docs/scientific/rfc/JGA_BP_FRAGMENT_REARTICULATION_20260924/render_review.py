from pathlib import Path
import json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
O=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=json.loads((O/'CLASSIFICATION_FREEZE.json').read_text())
assert sha(O/'CLASSIFICATIONS.json')==f['classification_sha256']
reasons={r['boundary_id']:(r['classification'],r['reason']) for r in json.loads((O/'CLASSIFICATIONS.json').read_text())}
# Final diagnostic pages reuse inspected curves with classifications; no PLP involved.
source=(O/'inspect_boundaries.py').read_text().replace('top=.9,bottom=.08','top=.9,bottom=.12')
source=source.replace("fig.savefig(O/f\"{b['boundary_id']}_INSPECT.png\",dpi=110);plt.close(fig)","""
 cls,reason=reasons[b['boundary_id']]
 for tx in fig.texts:
  if 'UNCLASSIFIED acoustic inspection' in tx.get_text():tx.set_text(tx.get_text().replace('UNCLASSIFIED acoustic inspection',cls))
 # Candidate front regions are visual annotations of the reviewed signal, not new emitted onset coordinates.
 regions={'FR04':(-40,-5),'FR05':(-45,-10),'FR11':(-80,-25),'FR12':(-65,-10)}
 if b['boundary_id'] in regions:
  a0,a1=regions[b['boundary_id']]
  for ax in axs[:4]:ax.axvspan(a0,a1,color='#dcac55',alpha=.13)
 import textwrap
 fig.text(.08,.014,'\\n'.join(textwrap.wrap(reason,145)),fontsize=8)
 finalpdf.savefig(fig);fig.savefig(O/f"{b['boundary_id']}_FINAL.png",dpi=110);plt.close(fig)
""")
with PdfPages(O/'SAME_PITCH_FRAGMENT_VS_REARTICULATION.pdf') as finalpdf:exec(compile(source,str(O/'inspect_boundaries.py'),'exec'))

assert sha(O/'CLASSIFICATIONS.json')==f['classification_sha256']
