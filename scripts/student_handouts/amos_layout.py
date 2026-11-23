"""Print layout recovered from the published Amos ReportLab builder."""
from reportlab.graphics.barcode import qr
from reportlab.graphics.renderPDF import draw
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

WIDTH, HEIGHT, MARGIN = 612, 792, 46


def linked(text, url):
    return '<link href="' + url.replace('&', '&amp;') + '"><u>' + text + '</u></link>'


class PDF:
    def __init__(self, destination, file, title):
        self.c = Canvas(str(destination / file), pagesize=(WIDTH, HEIGHT), invariant=True)
        self.c.setTitle(title)
        self.c.setAuthor('Independent scripture study companion')
        self.page = 0

    def p(self, text, size=10.5, font='Body', width=520):
        style = ParagraphStyle('text', fontName=font, fontSize=size,
                               leading=size * 1.4, textColor=HexColor('#222222'))
        paragraph = Paragraph(text, style)
        _, height = paragraph.wrap(width, 720)
        self.y -= height
        paragraph.drawOn(self.c, MARGIN, self.y)

    def gap(self, points=10):
        self.y -= points

    def start(self, title, subtitle):
        self.page += 1
        self.y = 744
        self.p('STUDENT STUDY  /  NOVEMBER 23–29, 2026', 8, 'Bold')
        self.gap(12)
        self.p(title, 23, 'Serif')
        self.gap(8)
        self.p(subtitle, 10)
        self.gap(16)

    def head(self, label, title):
        self.p(label.upper(), 8, 'Bold')
        self.gap(6)
        self.p(title, 16, 'Serif')
        self.gap(10)

    def link(self, title, url):
        self.p(linked(title, url), 9.5, 'Bold')
        self.gap(8)

    def lines(self, number=2):
        self.gap(18)
        self.c.setStrokeColor(HexColor('#B5B5B5'))
        self.c.setLineWidth(0.4)
        for _ in range(number):
            self.c.line(MARGIN, self.y, WIDTH - MARGIN, self.y)
            self.gap(20)
        self.gap(8)

    def resource(self, label, title, url, note):
        top = self.y
        widget = qr.QrCodeWidget(url)
        _, _, width, height = widget.getBounds()
        box = Drawing(66, 66, transform=[66 / width, 0, 0, 66 / height, 0, 0])
        box.add(widget)
        draw(box, self.c, WIDTH - MARGIN - 66, top - 66)
        self.p(label, 7.5, 'Bold', 440)
        self.gap(5)
        self.p(linked(title, url), 9.5, 'Bold', 440)
        self.gap(5)
        self.p(note, 9, 'Body', 440)
        self.y = min(self.y, top - 66) - 12

    def end(self, path):
        if self.y <= 52:
            raise ValueError(f'{path}, page {self.page}: content too close to footer ({self.y:.1f})')
        self.c.setStrokeColor(HexColor('#B5B5B5'))
        self.c.line(MARGIN, 43, WIDTH - MARGIN, 43)
        self.c.setFillColor(HexColor('#555555'))
        self.c.setFont('Body', 7)
        self.c.drawString(MARGIN, 30, 'Independent study companion • Personal answers stay private')
        self.c.drawRightString(WIDTH - MARGIN, 30, f'{path} / {self.page}')
        self.c.showPage()

    def save(self):
        self.c.save()
