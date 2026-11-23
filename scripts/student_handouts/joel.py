"""Editable reconstruction of the original two-page Joel print layouts."""
import json
from html import escape
from pathlib import Path

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.renderPDF import draw
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


def build(source: Path, target: Path):
    book = json.loads(source.read_text(encoding='utf-8'))
    canvas = Canvas(str(target), pagesize=(612, 792), invariant=True)
    canvas.setTitle(book['title'])
    canvas.setAuthor('Come, Follow Me study companion')
    for number, rows in enumerate(book['pages'], 1):
        canvas.setFillColor(HexColor('#222222'))
        canvas.rect(46, 757, 32, 3, stroke=0, fill=1)
        previous_bottom = 754
        for item in rows:
            if 'line' in item:
                if not 47 <= item['line'] <= previous_bottom:
                    raise ValueError(f'{source.name}, page {number}: writing line overlaps content')
                previous_bottom = item['line']
                canvas.setStrokeColor(HexColor('#B5B5B5'))
                canvas.setLineWidth(0.4)
                canvas.line(46, item['line'], 566, item['line'])
            elif 'qr' in item:
                if not 47 <= item['bottom'] < 680:
                    raise ValueError(f'{source.name}, page {number}: QR code outside page body')
                widget = QrCodeWidget(item['qr'])
                _, _, w, h = widget.getBounds()
                box = Drawing(68, 68, transform=[68 / w, 0, 0, 68 / h, 0, 0])
                box.add(widget)
                draw(box, canvas, 498, item['bottom'])
            else:
                size = item['size']
                color = '#555555' if item.get('muted') else '#222222'
                style = ParagraphStyle('Joel', fontName=item['font'], fontSize=size,
                                       leading=size * 1.42, textColor=HexColor(color))
                content = '<br/>'.join(escape(line) for line in item['text'].splitlines())
                if 'url' in item:
                    content = f'<link href="{escape(item["url"])}"><u>{content}</u></link>'
                paragraph = Paragraph(content, style)
                _, height = paragraph.wrap(item.get('width', 520), 720)
                bottom = item['top'] - height
                if bottom < 50 or item['top'] > previous_bottom:
                    raise ValueError(f'{source.name}, page {number}: needs space for {item["text"]!r}')
                paragraph.drawOn(canvas, 46, bottom)
                previous_bottom = bottom
        canvas.setStrokeColor(HexColor('#B5B5B5'))
        canvas.line(46, 43, 566, 43)
        canvas.setFillColor(HexColor('#555555'))
        canvas.setFont('Body', 7)
        canvas.drawString(46, 30, 'Unofficial companion • Supplements Come, Follow Me • Personal answers stay private')
        canvas.drawRightString(566, 30, f'{book["path_label"]}  /  {number}')
        canvas.showPage()
    canvas.save()
