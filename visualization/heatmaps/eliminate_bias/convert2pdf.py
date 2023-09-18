import os

folder = 'swarm_original_score'
svg_files = os.listdir(folder)
print(svg_files)

# put all svg files to one pdf file
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfMerger

merger = PdfMerger()
for svg_file in svg_files:
    drawing = svg2rlg(folder + '/' + svg_file)
    pdf_file = svg_file.replace('.svg', '.pdf')
    renderPDF.drawToFile(drawing, pdf_file)
    merger.append(pdf_file)
merger.write("swarm_original_score.pdf")
merger.close()
