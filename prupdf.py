from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
style = getSampleStyleSheet()
pdf = SimpleDocTemplate("test.pdf")
story = []
text = "Paragraphs are quite easy to create with Platypus, and Platypus handles things like word wrapping for you. There's not a lot of coding work involved if you wish to create something simple."
for x in xrange(25):
      para = Paragraph(text, style["Normal"])
      story.append(para)
      story.append(Spacer(inch * .5, inch * .5))
for tam_z in ["8.5", "10.0", "11.5"]:
      para = Paragraph("<font size='%s'>This is <b>%s</b>.</font>" % (tam_z, tam_z), style["Normal"])
      story.append(para)
      story.append(Spacer(inch * .5, inch * .5))     

for color in ["red", "green", "blue"]:
      para = Paragraph("<font color='%s'>This is <b>%s</b>.</font>" % (color, color), style["Normal"])
      story.append(para)
      story.append(Spacer(inch * .5, inch * .5))     

pdf.build(story)
