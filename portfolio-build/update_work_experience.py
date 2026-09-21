"""Render the complete recorded work history using the portfolio's existing cards."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parent.parent
roles = json.loads((ROOT / 'portfolio-build/work_experience.json').read_text())
cards = []
for role in roles:
    duties = ''.join('<div class="bullet"><span><strong>' + html.escape(label) + ':</strong> ' + html.escape(text) + '</span></div>' for label, text in role['duties'])
    tools = ''.join('<span class="metric">' + html.escape(tool) + '</span>' for tool in role['tools'])
    cards.append('<article class="card exp reveal"><div class="meta"><strong>' + html.escape(role['company']) + '</strong>' + html.escape(role['location']) + '<br>' + html.escape(role['dates']) + '</div><div><h3>' + html.escape(role['title']) + '</h3><div class="bullets">' + duties + '</div><div class="metrics">' + tools + '</div></div></article>')
section = '<section id="experience"><div class="wrap"><div class="head reveal"><div><div class="kicker">Professional experience</div><h2>My complete work experience.</h2></div><p class="note">Operations, retail team leadership and general banking: responsibilities, tools and practical contributions from each role.</p></div><div class="expList">' + ''.join(cards) + '</div></div></section>'
target = ROOT / 'index.html'
source, count = re.subn(r'<section id="experience">.*?</section>', lambda _: section, target.read_text(), count=1, flags=re.S)
if count != 1:
    raise SystemExit('Could not locate the experience section.')
target.write_text(source)
print(f'Updated {len(roles)} roles and {sum(len(role["duties"]) for role in roles)} responsibilities.')
