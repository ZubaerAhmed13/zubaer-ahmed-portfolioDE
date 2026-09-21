"""Embed the responsive presentation and interactions in the single-file site."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent


def apply_design(target):
    html = target.read_text(encoding="utf-8")
    css = (ROOT / 'portfolio-build/responsive_upgrade.css').read_text(encoding="utf-8")
    js = (ROOT / 'portfolio-build/portfolio_interactions.js').read_text(encoding="utf-8")
    html = re.sub(r'\s*<style id="responsive-design">.*?</style>', '', html, flags=re.S)
    html = html.replace('</head>', f'<style id="responsive-design">\n{css}</style>\n</head>', 1)

    # Replace the original unified script and any legacy project-preview binding.
    html = re.sub(r'<script(?: id="(?:portfolio-interactions|business-value-project-preview)")?>.*?</script>\s*', '', html, flags=re.S)
    html = html.replace('</body>', f'<script id="portfolio-interactions">\n{js}</script>\n</body>', 1)

    if 'id="readingProgress"' not in html:
        html = html.replace('</header>', '<div class="readingTrack" aria-hidden="true"><span id="readingProgress"></span></div></header>', 1)
    html = html.replace('<button class="icon" id="theme" aria-label="Toggle theme">◐</button>', '<button class="icon" id="theme" type="button" aria-label="Switch to dark theme" aria-pressed="false"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16Z" fill="currentColor" stroke="none"/></svg></button>')
    html = html.replace('<button class="icon menu" id="menu" aria-label="Open navigation">☰</button>', '<button class="icon menu" id="menu" type="button" aria-label="Open navigation" aria-haspopup="dialog" aria-controls="navigationDialog" aria-expanded="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10"/></svg></button>')
    html = html.replace('<button class="smallbtn" data-recruiter>', '<button class="smallbtn" type="button" data-recruiter aria-haspopup="dialog">')
    old_cta = '<div class="cta"><a class="btn secondary" href="https://www.linkedin.com/in/zubaer-ahmed13/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a class="btn secondary" href="mailto:zubaerknight@gmail.com">Email ↗</a><a class="btn secondary" href="#experience">View experience ↓</a></div>'
    new_cta = '<div class="cta"><a class="btn primary" href="#experience">Explore my experience ↓</a><a class="btn secondary" href="https://www.linkedin.com/in/zubaer-ahmed13/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a class="btn secondary" href="mailto:zubaerknight@gmail.com">Email ↗</a></div>'
    html = html.replace(old_cta, new_cta)
    html = html.replace('7 active digital projects · 3 applied academic projects', '7 active digital projects · 4 applied academic projects')

    if '<div class="modalBack" id="recruiterModal"' in html:
        start = html.index('<div class="modalBack" id="recruiterModal"')
        end = html.index('<div class="lightbox"', start)
        original = html[start:end].strip()
        inner = original[original.index('>') + 1:-len('</div>')]
        html = html[:start] + '<dialog class="portfolioDialog" id="recruiterModal" aria-labelledby="recruiter-title">' + inner + '</dialog>\n' + html[end:]
    if '<div class="lightbox"' in html:
        html = re.sub(r'<div class="lightbox".*?<div class="toast" id="toast">Copied</div>', '''<dialog class="portfolioDialog photoDialog" id="lightbox" aria-label="Expanded course photo"><button class="close" type="button" data-close aria-label="Close photo">×</button><figure><img id="lightboxImg" alt="Expanded course photo"><figcaption id="lightboxCaption"></figcaption></figure></dialog>''', html, count=1, flags=re.S)
    if 'id="navigationDialog"' not in html:
        navigation = '''<dialog class="portfolioDialog navDialog" id="navigationDialog" aria-labelledby="navigationTitle"><div class="modal"><div class="modalHead"><div><div class="kicker">Take a look around</div><h2 id="navigationTitle">Explore my story.</h2></div><button class="close" type="button" data-close aria-label="Close navigation">×</button></div><p class="navIntro">Experience, ideas, and the work behind them.</p><nav class="menuLinks" aria-label="Mobile navigation"><a href="#top">Home <span aria-hidden="true">↗</span></a><a href="#experience">Experience <span aria-hidden="true">↗</span></a><a href="#projects">Projects <span aria-hidden="true">↗</span></a><a href="#skills">Skills <span aria-hidden="true">↗</span></a><a href="#education">Education <span aria-hidden="true">↗</span></a><a href="#contact">Contact <span aria-hidden="true">↗</span></a></nav><div class="menuSecondary"><a href="#case-studies">Case studies</a><a href="#certifications">Certifications</a><a href="#community">Languages &amp; volunteering</a></div><button class="smallbtn" type="button" data-recruiter aria-haspopup="dialog">30-second profile ↗</button></div></dialog>
<a class="backTop" id="backTop" href="#top" aria-label="Back to top" hidden>↑</a>
'''
        html = html.replace('<script id="portfolio-interactions">', navigation + '<script id="portfolio-interactions">', 1)
    target.write_text(html, encoding="utf-8")


if __name__ == '__main__':
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'index.html'
    apply_design(target)
    print(f'Responsive design applied: {target}')
