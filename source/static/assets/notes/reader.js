/* Ebook Reader Shared Behavior */

function toggleSolution(id) {
  const el = document.getElementById('sol-' + id);
  if (el) el.classList.toggle('active');
}

function copyCode(btn) {
  const pre = btn.closest('.code-block-wrapper').querySelector('pre');
  if (!pre) return;
  navigator.clipboard.writeText(pre.textContent).then(() => {
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
  });
}

// ── EPUB 3 EXPORT ─────────────────────────────────────────────────────────────
async function exportChapterEPUB() {
  if (typeof JSZip === 'undefined') {
    alert('JSZip not loaded. Check your internet connection.');
    return;
  }
  const meta = window.EBOOK_META || { topicId: '0.0', topicTitle: 'Untitled', chapterLabel: 'Topic' };
  const zip = new JSZip();

  const annotations = [];
  let annotIdx = 0;
  document.querySelectorAll('.annot').forEach(el => {
    const tip = el.querySelector('.tip');
    if (!tip) return;
    annotIdx++;
    const termText = el.childNodes[0].textContent.trim();
    const noteText = tip.textContent.replace(/\s+/g, ' ').trim();
    annotations.push({
      "@type": "Annotation",
      "id": `#ann-${annotIdx}`,
      "motivation": "commenting",
      "creator": { "type": "Person", "name": "Aayat-AP-Prep" },
      "body": { "type": "TextualBody", "value": noteText, "format": "text/plain", "language": "en" },
      "target": {
        "source": "OEBPS/ch1.xhtml",
        "selector": { "type": "TextQuoteSelector", "exact": termText }
      }
    });
  });

  const profNotes = [];
  let noteIdx = 0;
  document.querySelectorAll('.prof-note').forEach(el => {
    noteIdx++;
    const label = el.querySelector('.prof-note-label');
    const text = el.textContent.replace(label ? label.textContent : '', '').trim();
    const labelText = label ? label.textContent.trim() : `Note ${noteIdx}`;
    profNotes.push({ id: `en-${noteIdx}`, label: labelText, text });
  });

  let footnotesHtml = '';
  document.querySelectorAll('.annot').forEach((el, i) => {
    const tip = el.querySelector('.tip');
    if (!tip) return;
    const noteId = `fn-${i + 1}`;
    footnotesHtml += `<aside id="${noteId}" epub:type="footnote" role="doc-footnote"><p>${tip.innerHTML.replace(/<[^>]+>/g, ' ').trim()}</p></aside>\n`;
  });

  const chapterBody = document.querySelector('.chapter-body');
  let chapterContent = chapterBody ? chapterBody.innerHTML : document.body.innerHTML;
  chapterContent = chapterContent.replace(/<button[^>]*>.*?<\/button>/gs, '');
  chapterContent = chapterContent.replace(/class="tip"[^>]*/g, 'style="display:none"');
  chapterContent = chapterContent.replace(/\son\w+="[^"]*"/g, '');

  const endnotesHtml = profNotes.map(n =>
    `<li id="${n.id}" epub:type="endnote"><strong>${n.label}</strong><p>${n.text}</p></li>`
  ).join('\n');

  const chapterXhtml = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<meta charset="UTF-8"/>
<title>${meta.chapterLabel} — ${meta.topicTitle}</title>
<style>
  body { font-family: "Times New Roman", Georgia, serif; font-size: 1em; line-height: 1.8; color: #1a1a1a; max-width: 680px; margin: 0 auto; padding: 40px 20px; }
  h1,h2,h3,h4 { font-family: Arial, sans-serif; color: #000; }
  h1 { font-size: 2em; border-bottom: 2px solid #800000; padding-bottom: 10px; }
  h3 { font-size: 1.1em; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #ddd; padding-bottom: 4px; margin-top: 2em; }
  pre { background: #1e1e24; color: #f8f8f2; padding: 16px; border-radius: 4px; font-size: 0.82em; overflow-x: auto; }
  code { font-family: "Courier New", monospace; font-size: 0.88em; background: rgba(0,0,0,0.06); padding: 1px 4px; }
  aside[epub|type~="footnote"] { margin: 1em 0; padding: 8px 12px; border-left: 3px solid #800000; background: #fffbf0; font-size: 0.88em; }
  sup.noteref a { color: #800000; text-decoration: none; font-size: 0.8em; }
</style>
</head>
<body>
<article epub:type="chapter">
<h1>${meta.chapterLabel}: ${meta.topicTitle}</h1>
<p><em>AP Cybersecurity, Annotated Academic Edition (2026)</em></p>
${chapterContent}
<section epub:type="footnotes">
<h3>Chapter Footnotes</h3>
${footnotesHtml}
</section>
</article>
</body>
</html>`;

  const endnotesXhtml = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><meta charset="UTF-8"/><title>Professor's Endnotes, ${meta.chapterLabel}</title>
<style>body{font-family:Georgia,serif;max-width:680px;margin:0 auto;padding:40px 20px;line-height:1.75;}h2{font-family:Arial,sans-serif;border-bottom:2px solid #800000;padding-bottom:8px;}ol{padding-left:20px;}li{margin-bottom:1.2em;}strong{color:#800000;display:block;}</style>
</head>
<body>
<section epub:type="endnotes">
<h2>Professor's Endnotes</h2>
<ol>${endnotesHtml}</ol>
</section>
</body>
</html>`;

  const annotationsJson = JSON.stringify({
    "@context": "http://www.w3.org/ns/anno.jsonld",
    "id": "annotations-ch1.json",
    "type": "AnnotationCollection",
    "label": `${meta.chapterLabel} Annotations`,
    "total": annotations.length,
    "items": annotations
  }, null, 2);

  const opf = `<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="en">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:identifier id="uid">urn:uuid:ap-cybersecurity-${meta.topicId}-2026</dc:identifier>
  <dc:title>AP Cybersecurity, ${meta.chapterLabel}: ${meta.topicTitle}</dc:title>
  <dc:creator>Aayat-AP-Prep</dc:creator>
  <dc:language>en</dc:language>
  <dc:date>2026</dc:date>
  <meta property="dcterms:modified">2026-01-01T00:00:00Z</meta>
</metadata>
<manifest>
  <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
  <item id="ch1" href="ch1.xhtml" media-type="application/xhtml+xml"/>
  <item id="endnotes" href="endnotes.xhtml" media-type="application/xhtml+xml"/>
  <item id="annotations" href="annotations.json" media-type="application/ld+json" properties="annotations"/>
</manifest>
<spine>
  <itemref idref="nav"/>
  <itemref idref="ch1"/>
  <itemref idref="endnotes"/>
</spine>
</package>`;

  const nav = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><meta charset="UTF-8"/><title>Navigation</title></head>
<body>
<nav epub:type="toc" id="toc">
<h2>Contents</h2>
<ol>
  <li><a href="ch1.xhtml">${meta.chapterLabel}: ${meta.topicTitle}</a></li>
  <li><a href="endnotes.xhtml">Professor's Endnotes</a></li>
</ol>
</nav>
</body>
</html>`;

  zip.file('mimetype', 'application/epub+zip', { compression: 'STORE' });
  zip.file('META-INF/container.xml',
    '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>');
  zip.file('OEBPS/content.opf', opf);
  zip.file('OEBPS/nav.xhtml', nav);
  zip.file('OEBPS/ch1.xhtml', chapterXhtml);
  zip.file('OEBPS/endnotes.xhtml', endnotesXhtml);
  zip.file('OEBPS/annotations.json', annotationsJson);

  const blob = await zip.generateAsync({ type: 'blob', mimeType: 'application/epub+zip' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `AP_Cybersecurity_${meta.topicId}_${meta.topicTitle.replace(/\s+/g, '_')}.epub`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

// ── OKULAR XML SIDECAR ───────────────────────────────────────────────────────
function downloadOkularSidecar() {
  const meta = window.EBOOK_META || { topicId: '0.0', topicTitle: 'Untitled' };
  const profNotes = [];
  document.querySelectorAll('.prof-note').forEach((el, i) => {
    const label = el.querySelector('.prof-note-label');
    const text = el.textContent.replace(label ? label.textContent : '', '').trim();
    const labelText = label ? label.textContent.trim() : `Note ${i + 1}`;
    profNotes.push({ label: labelText, text, y: 100 + i * 180 });
  });

  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  const annotationsXml = profNotes.map(n => `  <annotation type="2" modifyDate="" creationDate="" flags="4" color="#f5a623" lineWidth="1">
    <base transformationMatrix="1,0,0,1,50,${n.y}" boundingRect="50,${n.y},250,${n.y + 120}" page="0"/>
    <popup windowTitle="${esc(n.label)}" flags="0" geometry="50,${n.y + 10},400,80">
      <text>${esc(n.text).substring(0, 500)}</text>
    </popup>
  </annotation>`).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE okular-document>
<okular-document syntaxVersion="1">
  <annotationList>
${annotationsXml}
  </annotationList>
</okular-document>`;

  const blob = new Blob([xml], { type: 'application/xml' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `Topic_${meta.topicId}_${meta.topicTitle.replace(/\s+/g, '_')}.okular`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

document.addEventListener('DOMContentLoaded', () => {
  if (window.Prism) Prism.highlightAll();
});
