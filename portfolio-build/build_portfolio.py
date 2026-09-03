from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "index.html"
CSS = (ROOT / "portfolio-build" / "project_upgrade.css").read_text(encoding="utf-8")
SECTION = (ROOT / "portfolio-build" / "project_section.html").read_text(encoding="utf-8").strip()

html = TARGET.read_text(encoding="utf-8")

# Replace the complete existing Projects section. Requiring a following section
# prevents a broad regex from consuming the rest of the page if the markup changes.
pattern = re.compile(
    r'<section\s+id=["\']projects["\'][^>]*>.*?</section>(?=\s*<section\b)',
    re.IGNORECASE | re.DOTALL,
)
html, count = pattern.subn(SECTION, html, count=1)
if count != 1:
    raise SystemExit("Build stopped: could not safely identify exactly one #projects section.")

marker_start = "/* BEGIN BUSINESS VALUE PROJECT UPGRADE */"
marker_end = "/* END BUSINESS VALUE PROJECT UPGRADE */"
css_block = f"\n{marker_start}\n{CSS.rstrip()}\n{marker_end}\n"
if marker_start not in html:
    pos = html.find("</style>")
    if pos < 0:
        raise SystemExit("Build stopped: no </style> anchor found for project styles.")
    html = html[:pos] + css_block + html[pos:]

# Self-contained preview binding. It is intentionally wrapped in an IIFE so it
# can coexist with an older portfolio preview handler without global collisions.
preview_js = r'''<script id="business-value-project-preview">
(()=>{
  const tabs=[...document.querySelectorAll('#projects .showcaseTab')];
  const frame=document.getElementById('showcaseFrame');
  const open=document.getElementById('showcaseOpen');
  const label=document.getElementById('previewLabel');
  const placeholder=document.getElementById('previewPlaceholder');
  const load=document.getElementById('loadPreview');
  if(!tabs.length||!frame||!open||!label||!placeholder||!load)return;
  let url=tabs[0].dataset.url||'', name=tabs[0].dataset.label||'Project';
  tabs.forEach(tab=>tab.addEventListener('click',()=>{
    tabs.forEach(x=>{x.classList.remove('active');x.setAttribute('aria-pressed','false')});
    tab.classList.add('active');tab.setAttribute('aria-pressed','true');
    url=tab.dataset.url||'';name=tab.dataset.label||'Project';label.textContent=name;open.href=url;
    frame.hidden=true;frame.removeAttribute('src');placeholder.hidden=false;load.textContent='Load live preview';
  }));
  load.addEventListener('click',()=>{if(!url)return;frame.title='Live project preview — '+name;frame.src=url;frame.hidden=false;placeholder.hidden=true;});
})();
</script>'''
if 'id="business-value-project-preview"' not in html:
    pos = html.lower().rfind("</body>")
    if pos < 0:
        raise SystemExit("Build stopped: no </body> anchor found for preview behaviour.")
    html = html[:pos] + preview_js + "\n" + html[pos:]

# Release checks: these are intentionally content-based and fail closed.
required = [
    'Financial Workstation', 'LifeOS', 'VideoFlow Professional', 'VideoFlow Android',
    'PDF Toolkit', 'Persona AI', 'Recruiter-Focused Portfolio',
    'FlexyLyn Childcare Platform', 'Samsung Innovation Analysis', 'Campus Board Game Night',
    'AI as execution leverage, not a substitute for judgement.'
]
missing = [item for item in required if item not in html]
if missing:
    raise SystemExit("Build stopped: required project content missing: " + ", ".join(missing))
if html.count('id="projects"') != 1:
    raise SystemExit("Build stopped: #projects must exist exactly once.")

TARGET.write_text(html, encoding="utf-8")
print(f"Portfolio upgraded successfully: {TARGET} ({len(html):,} characters)")
