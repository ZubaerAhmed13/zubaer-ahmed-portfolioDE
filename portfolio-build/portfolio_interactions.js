(() => {
  'use strict';
  const root = document.documentElement;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const theme = document.getElementById('theme');
  function updateThemeButton() {
    const dark = root.dataset.theme === 'dark';
    theme.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    theme.setAttribute('aria-pressed', String(dark));
  }
  try {
    const saved = localStorage.getItem('za-theme');
    if (saved === 'dark' || saved === 'light') root.dataset.theme = saved;
  } catch (_) {}
  updateThemeButton();
  theme.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('za-theme', root.dataset.theme); } catch (_) {}
    updateThemeButton();
  });

  const menuButton = document.getElementById('menu');
  const navigation = document.getElementById('navigationDialog');
  const recruiter = document.getElementById('recruiterModal');
  const lightbox = document.getElementById('lightbox');
  const dialogs = [...document.querySelectorAll('.portfolioDialog')];
  function openDialog(dialog) {
    if (dialog.open) return;
    dialogs.forEach(other => { if (other.open) other.close(); });
    dialog.showModal();
    document.body.classList.add('scrollLocked');
    menuButton.setAttribute('aria-expanded', String(navigation.open));
    dialog.querySelector('[data-close]')?.focus({ preventScroll: true });
    if (!reducedMotion.matches) dialog.animate(
      [{ opacity: 0, transform: 'translateY(12px) scale(.985)' }, { opacity: 1, transform: 'none' }],
      { duration: 190, easing: 'cubic-bezier(.2,.8,.2,1)' }
    );
  }
  dialogs.forEach(dialog => {
    dialog.querySelectorAll('[data-close]').forEach(button => button.addEventListener('click', () => dialog.close()));
    dialog.addEventListener('close', () => {
      document.body.classList.toggle('scrollLocked', dialogs.some(item => item.open));
      menuButton.setAttribute('aria-expanded', String(navigation.open));
    });
    // A click outside the actual dialog closes its native backdrop.
    dialog.addEventListener('click', event => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    });
  });
  menuButton.addEventListener('click', () => openDialog(navigation));
  document.querySelectorAll('[data-recruiter]').forEach(button => button.addEventListener('click', () => openDialog(recruiter)));
  navigation.querySelectorAll('a[href^="#"]').forEach(link => link.addEventListener('click', () => {
    navigation.close();
    const target = document.querySelector(link.getAttribute('href'));
    if (target) requestAnimationFrame(() => {
      const heading = target.querySelector('h1,h2') || target;
      heading.tabIndex = -1;
      heading.focus({ preventScroll: true });
    });
  }));

  const tabs = [...document.querySelectorAll('.showcaseTab')];
  const frame = document.getElementById('showcaseFrame');
  const projectLink = document.getElementById('showcaseOpen');
  const previewLabel = document.getElementById('previewLabel');
  const placeholder = document.getElementById('previewPlaceholder');
  const loadPreview = document.getElementById('loadPreview');
  let selectedTab = tabs[0];
  tabs.forEach(tab => tab.addEventListener('click', () => {
    selectedTab = tab;
    tabs.forEach(item => {
      item.classList.toggle('active', item === tab);
      item.setAttribute('aria-pressed', String(item === tab));
    });
    previewLabel.textContent = tab.dataset.label;
    projectLink.href = tab.dataset.url;
    frame.hidden = true;
    frame.removeAttribute('src');
    placeholder.hidden = false;
  }));
  loadPreview?.addEventListener('click', () => {
    if (!selectedTab?.dataset.url) return;
    frame.title = 'Live project preview — ' + selectedTab.dataset.label;
    frame.src = selectedTab.dataset.url;
    frame.hidden = false;
    placeholder.hidden = true;
  });

  const image = document.getElementById('lightboxImg');
  const caption = document.getElementById('lightboxCaption');
  document.querySelectorAll('.pic').forEach(photo => {
    const source = photo.querySelector('img');
    const label = photo.querySelector('.piccap')?.textContent || source.alt || 'Course photo';
    photo.tabIndex = 0;
    photo.setAttribute('role', 'button');
    photo.setAttribute('aria-label', 'Expand photo: ' + label);
    photo.setAttribute('aria-haspopup', 'dialog');
    const openPhoto = () => {
      image.src = source.src;
      image.alt = source.alt || label;
      caption.textContent = label;
      openDialog(lightbox);
    };
    photo.addEventListener('click', openPhoto);
    photo.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); openPhoto(); }
    });
  });
  document.getElementById('openGallery')?.addEventListener('click', () => {
    document.getElementById('gallery').scrollIntoView({ behavior: reducedMotion.matches ? 'instant' : 'smooth' });
    document.querySelector('.pic')?.focus({ preventScroll: true });
  });

  // Content is visible by default; short, one-time entrances are an enhancement.
  if ('IntersectionObserver' in window && !reducedMotion.matches) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        if (!reducedMotion.matches) entry.target.animate(
          [{ opacity: .3, transform: 'translateY(16px)' }, { opacity: 1, transform: 'none' }],
          { duration: 380, easing: 'cubic-bezier(.2,.8,.2,1)' }
        );
      });
    }, { threshold: .04 });
    document.querySelectorAll('.reveal').forEach(element => observer.observe(element));
  }
  reducedMotion.addEventListener('change', () => {
    if (reducedMotion.matches) document.getAnimations().forEach(animation => animation.cancel());
  });

  const progress = document.getElementById('readingProgress');
  const backTop = document.getElementById('backTop');
  const sectionLinks = [...document.querySelectorAll('.navlinks a, .menuLinks a')];
  const sections = ['top', 'experience', 'projects', 'skills', 'education', 'contact'].map(id => document.getElementById(id));
  let ticking = false;
  let activeId = '';
  function updateReadingPosition() {
    const distance = Math.max(1, root.scrollHeight - window.innerHeight);
    progress.style.transform = `scaleX(${Math.max(0, Math.min(1, window.scrollY / distance))})`;
    backTop.hidden = window.scrollY < 700;
    let current = sections[0].id;
    sections.forEach(section => { if (section.getBoundingClientRect().top <= 150) current = section.id; });
    if (window.innerHeight + window.scrollY >= root.scrollHeight - 4) current = sections.at(-1).id;
    if (current !== activeId) {
      activeId = current;
      sectionLinks.forEach(link => {
        if (link.hash === '#' + current) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }
    ticking = false;
  }
  function scheduleReadingUpdate() {
    if (!ticking) { ticking = true; requestAnimationFrame(updateReadingPosition); }
  }
  window.addEventListener('scroll', scheduleReadingUpdate, { passive: true });
  window.addEventListener('resize', scheduleReadingUpdate, { passive: true });
  if ('ResizeObserver' in window) new ResizeObserver(scheduleReadingUpdate).observe(document.querySelector('main'));
  updateReadingPosition();
  document.getElementById('year').textContent = new Date().getFullYear();
})();
