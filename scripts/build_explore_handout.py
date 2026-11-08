"""Build the optional print library from explore.html. Development only: reportlab."""
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from build_handout import ROOT, Tree, Node, plain, DeterministicCanvas, Lines

URL = 'https://spelibertatis.github.io/come-follow-me-study/explore.html'
DEST = ROOT / 'handouts/daniel-explore-further.pdf'
body = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=12, spaceAfter=4)
small = ParagraphStyle('small', parent=body, fontSize=8.5, leading=10, spaceAfter=3)
heading = ParagraphStyle('heading', parent=body, fontName='Times-Bold', fontSize=20, leading=23, spaceAfter=9)
subhead = ParagraphStyle('subhead', parent=heading, fontSize=13, leading=16, spaceBefore=8, spaceAfter=4)
linkstyle = ParagraphStyle('link', parent=small, splitLongWords=True)

def p(text, style=body):
    return Paragraph(escape(plain(text)), style)

def children(node, tag):
    return [c for c in node.children if isinstance(c, Node) and c.tag == tag]

def footer(c, doc):
    c.setLineWidth(.4); c.line(42,34,570,34)
    c.setFont('Helvetica',8)
    c.drawString(42,22,'Explore Further / Optional companion / Independent supplemental study')
    c.drawRightString(570,22,f'{doc.page} / 6')

def build():
    root=Tree((ROOT/'explore.html').read_text(encoding='utf-8')).root
    story=[]
    def resource(article):
        parts=[p(article.find('h3').text(),subhead)]
        for cls in ['byline','resource-meta','chapters-label','investigate','resource-question','access']:
            parts.append(p(article.find(cls=cls).text(),body if cls in ['investigate','resource-question'] else small))
        detail=article.find('details')
        if detail:
            parts.extend(p(c.text(),small) for c in children(detail,'p'))
        url=article.find('a').attrs['href']
        parts.append(Paragraph('<link href="'+escape(url,quote=True)+'">'+escape(url)+'</link>',linkstyle))
        parts.append(Spacer(1,3))
        story.append(KeepTogether(parts))
    def page(title):
        if story: story.append(PageBreak())
        story.append(p(title,heading))
    official=children(root.find(id='official'),'article')
    scholars=children(root.find(id='scholarship'),'article')
    assert len(official)==7 and len(scholars)==6, 'Review pagination when resources change'
    page('Explore Further / A. Scripture & Church teaching')
    story.append(p('Optional print companion. You can finish the 15-minute Daniel lesson without this library. Read an introduction, choose a question, and use printed scriptures to begin. Full external resources require later access to the web.'))
    story.append(p('Scripture and authoritative Church teachings are the primary doctrinal sources. Academic work adds historical and literary context; it does not replace them.',small))
    for a in official[:3]: resource(a)
    page('A. Scripture & Church teaching / continued')
    for a in official[3:]: resource(a)
    page('B. Videos & Supplemental Commentary')
    story.append(p('Independent commentary is supplemental, not official Church teaching. The video itself requires internet access; the questions below can begin a discussion on paper.'))
    for a in children(root.find(id='commentary'),'article'): resource(a)
    story.append(p('Choose a trail through the library',subhead))
    for trail in [
        'Life in ancient Babylon: Daniel 1; Holm; Beaulieu.',
        'Faith under pressure: Daniel 1, 3, 6; Be Not Afraid, Only Believe.',
        'The fiery furnace: Daniel 3; Prinsloo; Beaulieu.',
        'Daniel and the lions’ den: Daniel 6; Hebrews 11; Wilson.',
        'Literary connections: Valeta; Prinsloo; Tanner.',
        'Historical questions: Holm; Beaulieu; Patterson; Tanner.'
    ]: story.append(p(trail))
    story.extend([p('A question I want to investigate',subhead),p('What does the scripture say? What would I need to learn from another source? Sharing your writing is optional.'),Lines(3)])
    qr=Drawing(90,90);qr.add(QrCodeWidget(URL,barLevel='M',barBorder=4,barWidth=90,barHeight=90))
    t=Table([[qr,[p('Visit the online library',subhead),p('Scan when you have a device, or type the address below. No reading activity or personal notes are collected by this study site.',small)]]],colWidths=[108,408])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
    story.extend([Spacer(1,12),t,Paragraph('<link href="'+URL+'">'+URL+'</link>',linkstyle)])
    page('C. Historical & Academic Scholarship')
    story.append(p('Scholars may disagree about Daniel’s setting, authorship, composition, and interpretation. Read their reasons carefully; disputed proposals are not settled facts.',small))
    for a in scholars[:3]: resource(a)
    page('C. Historical & Academic Scholarship / continued')
    for a in scholars[3:]: resource(a)
    page('Advanced Research / optional')
    advanced=root.find(id='advanced')
    for node in advanced.children:
        if not isinstance(node,Node): continue
        if node.tag=='p' and 'eyebrow' not in node.attrs.get('class',''):
            story.append(p(node.text(),small))
        if node.tag=='details':
            story.append(p(node.find('summary').text(),subhead))
            for child in node.children:
                if not isinstance(child,Node):continue
                if child.tag=='p':story.append(p(child.text(),body))
                if child.tag=='dl':
                    for item in child.children:
                        if isinstance(item,Node):story.append(p(item.text(),subhead if item.tag=='dt' else body))
    story.append(p('Independent and supplemental. Not affiliated with or endorsed by The Church of Jesus Christ of Latter-day Saints. Linked publishers have their own access terms and privacy practices.',small))
    DEST.parent.mkdir(exist_ok=True)
    SimpleDocTemplate(str(DEST),pagesize=(612,792),leftMargin=42,rightMargin=42,topMargin=36,bottomMargin=44,title='Daniel: Explore Further - optional print companion',author='Independent Come, Follow Me study').build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=DeterministicCanvas)
    print(DEST)

if __name__=='__main__': build()
