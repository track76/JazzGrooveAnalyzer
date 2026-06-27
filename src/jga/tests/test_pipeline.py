from jga.pipeline.analysis_pipeline import AnalysisPipeline
from tkinter.filedialog import askopenfilename
from tkinter import Tk


root = Tk()
root.withdraw()

filepath = askopenfilename(
    title="Seleziona un file audio"
)

pipeline = AnalysisPipeline()

context = pipeline.analyze(filepath)

print("\n========== ANALYSIS LOG ==========\n")

for entry in context.log:
    print(entry.timestamp.strftime("%H:%M:%S"), "-", entry.message)