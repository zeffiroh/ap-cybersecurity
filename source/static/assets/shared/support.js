/* Support & sponsorship rendering */

(function () {
  /* The wording of the support panel. Not a per-deployment setting,
     so it lives here rather than cluttering config.js. */
  var SUPPORT_COPY = {
    heading: "Support this course",
    body: "If your classroom has a budget for materials, a contribution covers hosting, diagram licensing, and the work of keeping every unit aligned to the current framework. Any amount is welcome.",
    ctaLabel: "Support the course"
  };

  var thisScript = document.currentScript;

  /* The support page builds its own, fuller version of these
     blocks, so the injected panel would only duplicate it. */
  if (document.documentElement.hasAttribute("data-support-page")) return;

  var cfg = window.APCYBER_SUPPORT || {};
  if (!(cfg.buttonId || cfg.pageUrl)) return;

  var base = "";
  if (thisScript) {
    base = (thisScript.getAttribute("src") || "")
      .replace(/assets\/site-shared\/support\.js.*$/, "");
  }

  var css = ''
    + '.support-region{font-family:var(--font-sans);max-width:760px;margin:44px auto 56px;}'
    /* On a landing page the region sits inside the content column and lines
       up with the section headings above it rather than floating centred. */
    + '.site-main > .support-region{margin:40px 40px 48px;}'
    + '@media (max-width:900px){.site-main > .support-region{margin:32px 20px 40px;}}'
    + '.support-panel{border:1px solid var(--border-color);border-top:3px solid var(--accent-color);'
    + 'background:var(--surface);padding:24px 26px;}'
    + '.support-panel h2{font-family:var(--font-sans);font-size:15px;font-weight:600;'
    + 'letter-spacing:.01em;margin:0 0 10px;color:var(--text-primary);}'
    + '.support-panel p{font-family:var(--font-sans);font-size:13px;line-height:1.65;'
    + 'color:var(--text-muted);margin:0 0 18px;}'
    + '.support-cta{display:inline-block;background:var(--accent-color);color:#fff;'
    + 'text-decoration:none;font-size:13px;font-weight:600;padding:10px 22px;border:0;'
    + 'cursor:pointer;font-family:var(--font-sans);}'
    + '.support-cta:hover{background:var(--accent-dark);color:#fff;}'
    + '.support-cta:focus-visible{outline:2px solid var(--focus-ring,#1a5fb4);outline-offset:2px;}'
    + '.support-note{font-size:11.5px;color:var(--text-faint);margin:12px 0 0;}'
    + '.sponsor-card{display:block;border:1px solid var(--border-color);border-radius:6px;'
    + 'background:var(--surface);text-decoration:none;color:var(--text-primary);'
    + 'overflow:hidden;transition:all .2s ease;margin-bottom:26px;}'
    + '.sponsor-card:hover{border-color:var(--accent-color);'
    + 'box-shadow:0 6px 20px rgba(128,0,0,0.08);transform:translateY(-2px);}'
    + '.sponsor-card-head{background:var(--paper-bg);padding:14px 20px;'
    + 'border-bottom:1px solid var(--border-color);display:flex;'
    + 'justify-content:space-between;align-items:baseline;gap:12px;}'
    + '.sponsor-card-kicker{font-size:10px;letter-spacing:.09em;text-transform:uppercase;'
    + 'color:var(--text-faint);font-weight:700;}'
    + '.sponsor-card-by{font-size:11.5px;color:var(--text-muted);}'
    + '.sponsor-card-body{padding:16px 20px 18px;}'
    + '.sponsor-card-title{font-family:var(--font-sans);font-size:15px;font-weight:700;'
    + 'color:var(--text-primary);margin:0 0 7px;}'
    + '.sponsor-card-desc{font-family:var(--font-serif);font-size:13.5px;line-height:1.6;'
    + 'color:var(--text-muted);margin:0 0 12px;}'
    + '.sponsor-card-cta{font-family:var(--font-sans);font-size:11.5px;font-weight:700;'
    + 'letter-spacing:.06em;text-transform:uppercase;color:var(--accent-color);}'
    + '@media print{.support-region.sponsor-card{display:none;}}';

  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  var region = document.createElement('section');
  region.className = 'support-region';
  region.setAttribute('aria-label', 'Support this course');

  /* Which unit this page belongs to, so the right sponsor is shown.
     Topic folders sit under a "Unit_N_..." directory. */
  function currentUnitId() {
    var m = /\/Unit_(\d+)_/.exec(location.pathname);
    return m ? 'unit-' + m[1] : null;
  }

  function buildSponsorCard() {
    var unitId = currentUnitId();
    var unitSponsors = cfg.unitSponsors || {};
    var s = unitId ? unitSponsors[unitId] : null;
    var kicker = 'Sponsored · Where this goes next';

    if (!s || !s.name) {
      var course = cfg.courseSponsor || {};
      if (!course.name) return null;
      s = {
        name: course.name,
        title: course.name,
        blurb: course.blurb,
        url: course.url
      };
      kicker = 'Course sponsor';
    }

    var card = document.createElement(s.url ? 'a' : 'div');
    card.className = 'sponsor-card';
    if (s.url) {
      card.href = s.url;
      card.target = '_blank';
      card.rel = 'noopener noreferrer sponsored';
    }

    var head = document.createElement('div');
    head.className = 'sponsor-card-head';
    var k = document.createElement('span');
    k.className = 'sponsor-card-kicker';
    k.textContent = kicker;
    head.appendChild(k);
    var by = document.createElement('span');
    by.className = 'sponsor-card-by';
    by.textContent = s.name;
    head.appendChild(by);
    card.appendChild(head);

    var cbody = document.createElement('div');
    cbody.className = 'sponsor-card-body';
    var ct = document.createElement('p');
    ct.className = 'sponsor-card-title';
    ct.textContent = s.title || s.name;
    cbody.appendChild(ct);
    if (s.blurb) {
      var cd = document.createElement('p');
      cd.className = 'sponsor-card-desc';
      cd.textContent = s.blurb;
      cbody.appendChild(cd);
    }
    if (s.url) {
      var cc = document.createElement('p');
      cc.className = 'sponsor-card-cta';
      cc.textContent = 'Visit →';
      cbody.appendChild(cc);
    }
    card.appendChild(cbody);
    return card;
  }

  var sponsorCard = buildSponsorCard();
  if (sponsorCard) region.appendChild(sponsorCard);

  var panel = document.createElement('div');
  panel.className = 'support-panel';

  var h = document.createElement('h2');
  h.textContent = SUPPORT_COPY.heading;
  panel.appendChild(h);

  var p = document.createElement('p');
  p.textContent = SUPPORT_COPY.body;
  panel.appendChild(p);

  var a = document.createElement('a');
  a.className = 'support-cta';
  a.href = base + 'support.html';
  a.textContent = SUPPORT_COPY.ctaLabel;
  panel.appendChild(a);

  var note = document.createElement('p');
  note.className = 'support-note';
  note.textContent = 'You choose the amount. Every page, download, and activity stays available either way.';
  panel.appendChild(note);

  region.appendChild(panel);

  function addSidebarLink() {
    var sections = document.querySelectorAll('.site-sidebar .sidebar-section');
    var target = null;
    for (var i = 0; i < sections.length; i++) {
      var title = sections[i].querySelector('.sidebar-section-title');
      if (title && /resources|course-wide/i.test(title.textContent)) target = sections[i];
    }
    if (!target || target.querySelector('.sidebar-link-support')) return;
    var link = document.createElement('a');
    link.className = 'sidebar-link sidebar-link-support';
    link.href = base + 'support.html';
    var icon = document.createElement('span');
    icon.className = 'n';
    icon.textContent = '♥';
    link.appendChild(icon);
    link.appendChild(document.createTextNode('Support'));
    target.appendChild(link);
  }

  function mount() {
    /* The textbook and the landing pages each have their own content
       column; anything else falls back to the end of the document. */
    var book = document.querySelector('.book');
    var main = document.querySelector('.site-main');
    var footer = document.querySelector('.site-footer');
    if (book) {
      book.appendChild(region);
    } else if (main) {
      main.appendChild(region);
    } else if (footer && footer.parentNode) {
      footer.parentNode.insertBefore(region, footer);
    } else {
      document.body.appendChild(region);
    }
  }

  function init() {
    mount();
    addSidebarLink();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
