"""Build the portfolio CV from the same complete work history as the website."""
from pathlib import Path
from html import escape
import base64
import io
import json
import re
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'output/pdf/Zubaer_Ahmed_CV.pdf'
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
roles = json.loads((ROOT / 'portfolio-build/work_experience.json').read_text())
source = (ROOT / 'index.html').read_text()
match = re.search(r'<div class="portrait"><img[^>]*src="data:image/[^;]+;base64,([^\"]+)"', source)
portrait = None
if match:
    picture = Image.open(io.BytesIO(base64.b64decode(match.group(1)))).convert('RGB')
    picture.thumbnail((240, 320), Image.Resampling.LANCZOS)
    photo_buffer = io.BytesIO()
    picture.save(photo_buffer, format='JPEG', quality=90, optimize=True)
    photo_buffer.seek(0)
    portrait = ImageReader(photo_buffer)
navy = colors.HexColor('#153351')
blue = colors.HexColor('#21658c')
muted = colors.HexColor('#425366')
body = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=12.5, textColor=navy, spaceAfter=4)
small = ParagraphStyle('small', parent=body, fontSize=8.7, leading=11.5, textColor=muted)
heading = ParagraphStyle('heading', parent=body, fontName='Helvetica-Bold', fontSize=11, leading=14, spaceBefore=10, spaceAfter=7, textColor=blue, keepWithNext=True)
employer = ParagraphStyle('employer', parent=body, fontName='Helvetica-Bold', fontSize=10.5, leading=14, spaceBefore=8, spaceAfter=2, keepWithNext=True)
bullet = ParagraphStyle('bullet', parent=body, leftIndent=9, firstLineIndent=-9, spaceAfter=4)
story = []

def para(text, style=body):
    story.append(Paragraph(text, style))

def section(text):
    para(text, heading)

def job(role):
    para(escape(role['company']) + ' | ' + escape(role['title']), employer)
    para(escape(role['location']) + ' | ' + escape(role['dates']), small)
    for label, text in role['duties']:
        para('- <b>' + escape(label) + ':</b> ' + escape(text), bullet)
    para('<b>Tools:</b> ' + escape(' | '.join(role['tools'])), small)

def header(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(navy)
    if doc.page == 1:
        canvas.setFont('Helvetica-Bold', 23)
        canvas.drawString(44, height-48, 'Zubaer Ahmed')
        canvas.setFont('Helvetica', 9.5)
        canvas.drawString(44, height-66, 'Finance | Business Analysis | PMO | Operations')
        canvas.setFont('Helvetica', 8.5)
        canvas.drawString(44, height-83, 'Worms, Germany | +49 160 3027020 | zubaerknight@gmail.com')
        canvas.drawString(44, height-97, 'linkedin.com/in/zubaer-ahmed13 | Portfolio')
        canvas.linkURL('https://www.linkedin.com/in/zubaer-ahmed13/', (44,height-99,220,height-88))
        canvas.linkURL('https://zubaerahmed13.github.io/zubaer-ahmed-portfolioDE/', (221,height-99,285,height-88))
        if portrait:
            canvas.drawImage(portrait, width-97, height-106, width=53, height=70, preserveAspectRatio=True, anchor='c', mask='auto')
    else:
        canvas.setFont('Helvetica-Bold', 11)
        canvas.drawString(44, height-42, 'Zubaer Ahmed')
        canvas.setFont('Helvetica', 8.5)
        canvas.drawRightString(width-44, height-42, 'Detailed professional profile')
    canvas.setStrokeColor(colors.HexColor('#c7d9e5'))
    canvas.line(44, 39, width-44, 39)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(muted)
    canvas.drawString(44, 26, 'Zubaer Ahmed | Work experience and qualifications')
    canvas.drawRightString(width-44, 26, str(doc.page))
    canvas.restoreState()

# A complete history is intentionally presented over three readable pages.
story.append(Spacer(1, 54))
section('PROFILE')
para('M.A. Entrepreneurship student with a BBA in Finance and experience in German fulfilment operations, retail team leadership and general banking. Brings inventory and quality reporting, Excel-based tracking, customer communication, documentation and practical process-improvement experience. Expected graduation: <b>Mar 2028</b>.')
section('WORK EXPERIENCE')
job(roles[0])
job(roles[1])
story.append(PageBreak())
section('WORK EXPERIENCE - CONTINUED')
job(roles[2])
section('EDUCATION')
para('Master of Arts in Entrepreneurship | Hochschule Worms', employer)
para('Mar 2024 - Mar 2028 (expected) | Worms, Germany', small)
para('<b>Relevant courses:</b> Project &amp; Change Management; Creativity &amp; Innovation; Management &amp; Marketing of Innovations; Strategies of Internationalization; International Entrepreneurship; Leadership; Business Psychology; Intercultural Management.')
para('Bachelor of Business Administration - Finance | Stamford University Bangladesh', employer)
para('Completed May 2023 | Dhaka, Bangladesh | GPA: 3.55/4.00 | German-equivalent grade: 1.9', small)
para('<b>Relevant courses:</b> Financial Analysis &amp; Control; Management Accounting; Investment Analysis &amp; Portfolio Management; Financial Markets &amp; Institutions; Law &amp; Practice of Banking; Auditing; Insurance &amp; Risk Management.')
story.append(PageBreak())
section('SKILLS')
for label, text in [
    ('Microsoft Excel - Advanced', 'PivotTables; XLOOKUP/VLOOKUP; SUMIFS/COUNTIFS; IF; conditional formatting; data validation; charts and dashboards; data cleaning.'),
    ('Business and finance', 'Financial analysis; management accounting; business research; financial modelling; business planning.'),
    ('Office and collaboration', 'Word, PowerPoint, Outlook, Teams, SharePoint, Jira, Trello and Miro - Advanced; Slack and Canva - Intermediate.'),
    ('Systems', 'Core Banking Systems - Intermediate; WMS - operational use; Workday - Basic, employee use; SAP S/4HANA and SAP ERP FI - currently learning.'),
    ('Digital projects', 'Requirements definition; workflow design; business logic; AI-assisted prototyping; testing and QA; iterative development.'),
    ('Professional strengths', 'Reliable and adaptable; attention to detail; teamwork; customer communication; structured problem solving.'),
    ('Languages', 'Bangla - Native; English - Fluent/C1; German - A1; Hindi - Conversational.')
]: para('<b>' + escape(label) + ':</b> ' + escape(text))
section('ACADEMIC AND INDEPENDENT PROJECTS')
for label, text in [
    ('Lufthansa Group-linked academic collaboration', 'Two semesters through Hochschule Worms. Applied Design Thinking, research, ideation, prototyping, stakeholder testing and presentation. Contributed OpenLab learning-content pages, quiz and certificate concepts, idea-napkin and nudge-plan elements.'),
    ('Samsung Innovation Analysis', 'Three-person academic team analysed innovation strategy and developed recommendations on AI integration, platform expansion and manufacturing efficiency. Grade: 1.7.'),
    ('FlexyLyn Childcare Platform', 'Six-person academic business-plan team. Led market research and contributed to the go-to-market, financial and operational plan. Grade: 1.7.'),
    ('Campus Board Game Night and cross-cultural interviews', 'Four-person academic event-planning project; separate interview and research work on intercultural communication, with findings developed into a presentation.'),
    ('Independent digital projects', 'Financial Workstation, LifeOS, PDF Toolkit, VideoFlow Professional, VideoFlow Android, Persona AI and this portfolio. Requirements definition, workflow design, AI-assisted prototyping and testing; individual project stages are shown on the portfolio.')
]: para('<b>' + escape(label) + ':</b> ' + escape(text))
section('CERTIFICATIONS')
para('Project Management Foundations; Change Management; SAP S/4HANA Essential Training; Excel Essential Training (Microsoft 365); Word Essential Training (Microsoft 365); PowerPoint: Designing Better Slides; Introduction to ESG.')
section('VOLUNTEERING')
para('<b>Volunteer for Bangladesh:</b> Participated in "Fight for Trash" and "My Road My Responsibility" civic and environmental initiatives.')
para('<b>Stamford Anti-Drug Forum | 2022-2023:</b> Participated in awareness activities, seminars and campus programmes focused on substance-abuse prevention and student engagement.')
section('HOBBIES')
para('Hiking and travelling.')

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=44, rightMargin=44, topMargin=56, bottomMargin=52, title='Zubaer Ahmed - Complete Work Experience and Qualifications', author='Zubaer Ahmed')
doc.build(story, onFirstPage=header, onLaterPages=header)
print(OUTPUT)
