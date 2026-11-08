"""Build the static student PDF from the essential study HTML.

Development dependency: reportlab. No runtime network access or student input.
Run from any directory: python scripts/build_handout.py
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.lib import colors

ROOT=Path(__file__).resolve().parents[1]
URL='https://spelibertatis.github.io/come-follow-me-study/'
DEST=ROOT/'handouts/daniel-student-handout.pdf'

class Node:
    def __init__(self,tag='',attrs=None):
        self.tag=tag; self.attrs=dict(attrs or []); self.children=[]
    def text(self):
        return ''.join(c.text() if isinstance(c,Node) else c for c in self.children)
    def find(self,tag=None,cls=None,id=None):
        for c in self.children:
            if isinstance(c,Node):
                if (not tag or c.tag==tag) and (not cls or cls in c.attrs.get('class','').split()) and (not id or c.attrs.get('id')==id):
                    return c
                found=c.find(tag,cls,id)
                if found: return found
        return None

class Tree(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.root=Node(); self.stack=[self.root]; self.feed(text)
    def handle_starttag(self,tag,attrs):
        node=Node(tag,attrs); self.stack[-1].children.append(node)
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}: self.stack.append(node)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:
                self.stack=self.stack[:i]; break
    def handle_data(self,data): self.stack[-1].children.append(data)

def plain(text):
    return ' '.join(text.translate(str.maketrans({'’':"'",'‘':"'",'“':'"','”':'"','–':'-','—':' - ','…':'...','·':' / '})).split())

body=ParagraphStyle('body',fontName='Helvetica',fontSize=10.5,leading=14,spaceAfter=5)
small=ParagraphStyle('small',parent=body,fontSize=8.5,leading=11)
scripture=ParagraphStyle('scripture',parent=body,fontName='Times-Roman',fontSize=11.5,leading=14.5,leftIndent=10,borderPadding=4,spaceAfter=6)
heading=ParagraphStyle('heading',parent=body,fontName='Times-Bold',fontSize=18,leading=21,spaceBefore=7,spaceAfter=6)
title=ParagraphStyle('title',parent=heading,fontSize=26,leading=28,spaceBefore=0)

def p(text,style=body): return Paragraph(escape(plain(text)),style)
def labeled(label,text): return Paragraph('<b>'+escape(label)+'</b> '+escape(plain(text)),body)

class Lines(Flowable):
    def __init__(self,count=1): super().__init__(); self.count=count; self.height=count*19; self.width=516
    def draw(self):
        self.canv.setStrokeColor(colors.HexColor('#9a9a9a')); self.canv.setLineWidth(.4)
        for i in range(self.count): self.canv.line(0,self.height-16-i*19,self.width,self.height-16-i*19)

class DeterministicCanvas(canvas.Canvas):
    def __init__(self,*args,**kwargs):
        kwargs['invariant']=1
        super().__init__(*args,**kwargs)

def footer(c,doc):
    c.setStrokeColor(colors.black); c.setLineWidth(.4); c.line(42,34,570,34)
    c.setFont('Helvetica',8)
    c.drawString(42,22,'Independent supplemental study / Scripture quotations: King James Version')
    c.drawRightString(570,22,f'{doc.page} / 2')

def build():
    tree=Tree((ROOT/'index.html').read_text(encoding='utf-8')).root
    story=[]
    qr=QrCodeWidget(URL,barLevel='M',barBorder=4,barWidth=82,barHeight=82)
    drawing=Drawing(82,82); drawing.add(qr)
    intro=[p('Faith under pressure',title),p('DANIEL 1, 3 & 6 / ABOUT 15 MINUTES',small),p('How can you stay true to God when the world around you pulls another way?',body),p('Read, notice, and choose one small step. You can think quietly or write. No phone is needed.',small)]
    qrnote=[drawing,p('Online study + library',small)]
    top=Table([[intro,qrnote]],colWidths=[424,104]); top.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    story+=[top,Paragraph(f'<link href="{URL}">{URL.removeprefix("https://")}</link>',small),Spacer(1,5)]

    def chapter(number):
        section=tree.find(id=f'daniel-{number}')
        if not section: raise ValueError(f'Missing Daniel {number}')
        story.append(p(f'Daniel {number} / '+section.find('h2').text(),heading))
        story.append(labeled('Context (summary):',section.find(cls='intro').text()))
        paragraphs=[c for c in section.find(cls='section-body').children if isinstance(c,Node) and c.tag=='p']
        ref=next(c.text() for c in paragraphs if 'KING JAMES VERSION' in c.text())
        story.append(p(ref,small))
        for verse in section.find('blockquote').children:
            if isinstance(verse,Node) and verse.tag=='p': story.append(p(verse.text(),scripture))
        story.append(p(section.find(cls='word-note').text(),small))
        story.append(labeled('Notice:',section.find(cls='question').text()))
        outcome=section.find(cls='outcome')
        story.append(p(outcome.text(),small))
        # The paragraph immediately after outcome carries the source's caveat.
        i=paragraphs.index(outcome)
        if i+1<len(paragraphs): story.append(p(paragraphs[i+1].text(),small))
        nodes=section.find(cls='section-body').children
        for i,node in enumerate(nodes):
            if isinstance(node,Node) and node.tag=='h3' and node.text()=='Try it in your life':
                prompt=next(c for c in nodes[i+1:] if isinstance(c,Node) and c.tag=='p')
                story.append(labeled('Try:',prompt.text())); break
        story.append(Lines())

    chapter(1); chapter(3)
    story.append(PageBreak())
    story.append(p('Faith under pressure / continue',small))
    chapter(6)
    story.append(Spacer(1,12))
    story.append(p('Three stories. One next step.',heading))
    reflection=tree.find(id='reflection')
    story.append(p(reflection.find(cls='intro').text()))
    story.append(p('Choose one small practice for your week: respond respectfully, stand by a belief, or make time to pray. What could that look like in your life?'))
    story.append(p('A thought or question to take with me (optional):',body))
    story.append(Lines(4))
    story.append(Spacer(1,15))
    story.append(p('You can stop here.',heading))
    story.append(p('Keep one thought or question as you go into your week. Faith does not guarantee physical rescue; there is room for grief and unanswered questions.'))
    story.append(p('For another day',heading))
    story.append(p('Optional deeper study: read Daniel 1:3-20, 3:13-30, or 6:4-23. Look for the pressure, the response, and the outcome. The QR code on page 1 opens the online journey and its Explore Further library.'))
    story.append(p('Your writing is yours. Sharing it with the class is optional. This handout is independent and is not affiliated with or endorsed by The Church of Jesus Christ of Latter-day Saints.',small))
    DEST.parent.mkdir(exist_ok=True)
    doc=SimpleDocTemplate(str(DEST),pagesize=(612,792),leftMargin=42,rightMargin=42,topMargin=36,bottomMargin=44,title='Daniel: Faith under pressure - student handout',author='Independent Come, Follow Me study')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=DeterministicCanvas)
    print(DEST)

if __name__=='__main__': build()
