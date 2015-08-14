import os
from reportlab.lib.units import inch, mm
from timereg.models import MonthlyReport
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import landscape, A4
from timez.settings import BASE_DIR

__author__ = 'unic0arn'


class SimplePage(PageTemplate):
    def __init__(self):
        frameT = Frame( 25 * mm,
                        140 * mm,
                        160 * mm,
                        60 * mm,
                        id='normal')

        PageTemplate.__init__(
            self,
            id="SimplePage",
            frames = [frameT]
        )
def generate_report(response, rid):


    styles = getSampleStyleSheet()
    doc = BaseDocTemplate(response,
                          pageTemplates=[SimplePage()],
                          pagesize=landscape(A4))
    report = MonthlyReport.objects.get(pk = rid)
    imgpath = os.path.join(BASE_DIR, 'timereg/static/timereg/xpeedio_logo.png')

    im = Image(imgpath)

    Story = [im,
             Spacer(1,20),
             Paragraph("Hello World!",styles["Normal"]),
             Spacer(50,20),
             Paragraph("Hello World2!",styles["Normal"])]

    doc.build(Story)


    #
    # c = canvas.Canvas(response)
    # c.drawString(100,750,"Welcome to Reportlab!")
    # month = report.month
    #
    #
    #
    # c.drawString(100,710,str(month.max))
    # c.showPage()
    # c.save()

    return True