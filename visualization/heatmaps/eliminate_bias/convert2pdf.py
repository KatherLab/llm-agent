import os

folder = '/home/jeff/PycharmProjects/llm-agent/visualization/heatmaps/eliminate_bias/box_score_plot'
svg_files = os.listdir(folder)
print(svg_files)
# sort the svg files, if all_ is not the first, put it to the first
if 'all_' in svg_files:
    svg_files.remove('all_task_box_adjusted_score.svg')
    svg_files.insert(0, 'all_task_box_adjusted_score.svg')
svg_files = sorted(svg_files)
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

merger.write("box_score_plot.pdf")
merger.close()
