"""
Parses unit_quizbank_*.xml files and pre-renders artifacts to HTML
for injection into the frontend stimulus panel.
"""
import xml.etree.ElementTree as ET
import html as html_mod
import os, glob, re


# --------------------------------------------------------------------------- #
# Public API                                                                    #
# --------------------------------------------------------------------------- #

class QuizLoader:
    def __init__(self, quizbanks_dir: str = 'quizbanks'):
        self.units      : dict[str, dict] = {}   # unit_id → meta
        self.items      : dict[str, dict] = {}   # item_id → item
        self.unit_items : dict[str, list] = {}   # unit_id → [item_id, ...]
        self._load_all(quizbanks_dir)

    def _load_all(self, directory: str):
        for path in sorted(glob.glob(os.path.join(directory, '*.xml'))):
            self._load_file(path)

    def _load_file(self, path: str):
        tree = ET.parse(path)
        root = tree.getroot()
        uid   = root.get('unit_id')
        title = root.get('unit_title', uid)

        self.units[uid]      = {'id': uid, 'unit_id': uid, 'title': title}
        self.unit_items[uid] = []

        for ss in root.findall('stimulus_set'):
            stim_el  = ss.find('stimulus')
            stim     = self._parse_stimulus(stim_el)
            items_el = ss.find('items')
            for q in items_el.findall('question'):
                item = self._parse_question(q, stim, uid)
                self.items[item['id']]    = item
                self.unit_items[uid].append(item['id'])

        self.units[uid]['count'] = len(self.unit_items[uid])

    # ---------------------------------------------------------------------- #

    def get_items(self, unit_id: str) -> list:
        return [self.items[i] for i in self.unit_items.get(unit_id, [])]

    def get_item(self, item_id: str) -> dict | None:
        return self.items.get(item_id)

    def unit_list(self) -> list:
        return list(self.units.values())


# --------------------------------------------------------------------------- #
# XML parsing                                                                   #
# --------------------------------------------------------------------------- #

    def _parse_stimulus(self, el) -> dict:
        if el is None:
            return {}
        artifact_el = el.find('artifact')
        return {
            'type'        : _txt(el, 'type'),
            'label'       : _txt(el, 'label'),
            'context'     : _txt(el, 'context'),
            'artifact_html': render_artifact(artifact_el),
        }

    def _parse_question(self, q, stim: dict, unit_id: str) -> dict:
        meta = q.find('meta')
        sv   = q.find('skill_vector')
        am   = q.find('adaptive_meta')
        prim = sv.find('primary')  if sv is not None else None
        sec  = sv.find('secondary') if sv is not None else None

        choices = {c.get('key'): (c.text or '').strip()
                   for c in q.find('choices').findall('choice')}

        dr = {}
        dr_el = q.find('distractor_rationale')
        if dr_el is not None:
            dr = {c.get('key'): (c.text or '').strip()
                  for c in dr_el.findall('choice')}

        return {
            'id'         : q.get('id'),
            'unit_id'    : unit_id,
            'stimulus'   : stim,
            'topic_refs' : _txt(meta, 'topic_refs') if meta is not None else '',
            'lo_refs'    : _txt(meta, 'lo_refs')    if meta is not None else '',
            'skill_vector': {
                'primary': {
                    'skill' : prim.get('skill')         if prim is not None else '1.A',
                    'lo'    : prim.get('lo', '')        if prim is not None else '',
                    'weight': prim.get('weight', '1.0') if prim is not None else '1.0',
                },
                'secondary': {
                    'skill' : sec.get('skill')          if sec is not None else None,
                    'lo'    : sec.get('lo', '')         if sec is not None else '',
                    'weight': sec.get('weight', '0.0')  if sec is not None else '0.0',
                } if sec is not None else None,
            },
            'b_param'       : _txt(am, 'b_param',    '0.0')  if am is not None else '0.0',
            'a_param'       : _txt(am, 'a_param',    '1.0')  if am is not None else '1.0',
            'c_param'       : _txt(am, 'c_param',    '0.25') if am is not None else '0.25',
            'exposure_cap'  : int(_txt(am, 'exposure_cap', '3')) if am is not None else 3,
            'est_time'      : _txt(am, 'est_response_time_sec', '60') if am is not None else '60',
            'stem'          : _txt(q,  'stem'),
            'choices'       : choices,
            'correct_answer': q.find('answer').get('key') if q.find('answer') is not None else 'A',
            'explanation'   : _txt(q, 'explanation'),
            'distractor_rationale': dr,
        }


# --------------------------------------------------------------------------- #
# Helpers                                                                       #
# --------------------------------------------------------------------------- #

def _txt(el, tag: str, default: str = '') -> str:
    if el is None:
        return default
    child = el.find(tag)
    if child is None:
        return default
    return (child.text or '').strip()


def _h(s: str) -> str:
    """HTML-escape a string."""
    return html_mod.escape(str(s or ''))


def _inner(el) -> str:
    """All text content of an element (recursive)."""
    parts = [el.text or '']
    for child in el:
        parts.append(_inner(child))
        parts.append(child.tail or '')
    return ''.join(parts).strip()


# --------------------------------------------------------------------------- #
# Artifact → HTML renderers                                                     #
# --------------------------------------------------------------------------- #

def render_artifact(el) -> str:
    if el is None:
        return ''
    fmt = el.get('format', 'text')
    dispatch = {
        'email_thread'             : _render_email_thread,
        'email'                    : _render_email_single,
        'clipping'                 : _render_clipping,
        'chat_transcript'          : _render_chat,
        'log_file'                 : _render_log,
        'pacs_log'                 : _render_log,
        'rfid_log_plus_floorplan'  : _render_composite,
        'policy_memo'              : _render_policy,
        'annotated_policy'         : _render_policy,
        'composite'                : _render_composite,
        'composite_smishing_cert'  : _render_composite,
        'incident_plus_device_report': _render_composite,
        'social_profile'           : _render_social,
        'transcript'               : _render_transcript,
        'incident_report'          : _render_report_doc,
        'investigation_report'     : _render_report_doc,
        'cctv_incident_report'     : _render_report_doc,
        'visitor_signin_sheet'     : _render_composite,
        'cert_inspection'          : _render_cert,
        'annotated_policy'         : _render_policy,
    }
    fn = dispatch.get(fmt, _render_generic)
    return fn(el)


def _render_email_thread(el) -> str:
    parts = ['<div class="art-email-client"><div class="art-email-toolbar"><span class="art-app-label">📧 Email</span></div><div class="art-email-list">']
    for msg in el.findall('email'):
        seq = msg.get('seq', '')
        frm  = _h(_inner_tag(msg, 'from'))
        to   = _h(_inner_tag(msg, 'to'))
        date = _h(_inner_tag(msg, 'date'))
        subj = _h(_inner_tag(msg, 'subject'))
        body = _h(_inner_tag(msg, 'body'))
        parts.append(f'''
<div class="art-email-msg">
  <div class="art-email-hdr">
    <div><span class="art-lbl">From:</span> <code>{frm}</code></div>
    <div><span class="art-lbl">To:</span> <code>{to}</code></div>
    <div><span class="art-lbl">Date:</span> {date}</div>
    <div><span class="art-lbl">Subject:</span> <strong>{subj}</strong></div>
  </div>
  <pre class="art-email-body">{body}</pre>
</div>''')
    parts.append('</div></div>')
    return ''.join(parts)


def _render_email_single(el) -> str:
    frm  = _h(_inner_tag(el, 'from'))
    to   = _h(_inner_tag(el, 'to'))
    rto  = _h(_inner_tag(el, 'reply_to'))
    date = _h(_inner_tag(el, 'date'))
    subj = _h(_inner_tag(el, 'subject'))
    body = _h(_inner_tag(el, 'body'))
    att  = _inner_tag(el, 'attachment')
    # technical headers
    hdrs_el = el.find('technical_headers')
    hdrs_html = ''
    if hdrs_el is not None:
        rows = ''.join(
            f'<div><span class="art-lbl">{_h(h.get("name",""))}:</span> <code class="art-warn">{_h(_inner(h))}</code></div>'
            for h in hdrs_el.findall('header')
        )
        hdrs_html = f'<div class="art-tech-headers"><div class="art-lbl-section">⚙ Technical Headers</div>{rows}</div>'

    att_html = f'<div class="art-attachment">📎 {_h(att)}</div>' if att else ''
    return f'''
<div class="art-email-client">
  <div class="art-email-toolbar"><span class="art-app-label">📧 Email</span></div>
  <div class="art-email-msg">
    <div class="art-email-hdr">
      <div><span class="art-lbl">From:</span> <code>{frm}</code></div>
      <div><span class="art-lbl">To:</span> <code>{to}</code></div>
      {'<div><span class="art-lbl art-warn">Reply-To:</span> <code class="art-warn">' + _h(rto) + '</code></div>' if rto else ''}
      <div><span class="art-lbl">Date:</span> {date}</div>
      <div><span class="art-lbl">Subject:</span> <strong>{subj}</strong></div>
    </div>
    <pre class="art-email-body">{body}</pre>
    {att_html}
  </div>
  {hdrs_html}
</div>'''


def _render_clipping(el) -> str:
    outlet   = _h(_inner_tag(el, 'outlet'))
    date     = _h(_inner_tag(el, 'date'))
    headline = _h(_inner_tag(el, 'headline'))
    dateline = _h(_inner_tag(el, 'dateline'))
    body     = _h(_inner_tag(el, 'body'))
    return f'''
<div class="art-newspaper">
  <div class="art-paper-masthead">{outlet}</div>
  <div class="art-paper-date">{date}</div>
  <div class="art-paper-rule"></div>
  <h3 class="art-paper-headline">{headline}</h3>
  <p class="art-paper-body"><strong>{dateline}</strong> {body}</p>
</div>'''


def _render_chat(el) -> str:
    platform = _h(_inner_tag(el, 'platform') or el.get('platform', 'Chat'))
    date     = _h(_inner_tag(el, 'date') or '')
    msgs_el  = el.find('messages') or el
    rows = []
    for msg in msgs_el.findall('msg') or msgs_el.findall('message'):
        user = _h(msg.get('user', msg.get('speaker', 'User')))
        time = _h(msg.get('time', ''))
        text = _h((msg.text or '').strip())
        rows.append(f'<div class="art-chat-msg"><span class="art-chat-user">{user}</span><span class="art-chat-time">{time}</span><span class="art-chat-text">{text}</span></div>')
    return f'''
<div class="art-slack">
  <div class="art-slack-hdr">💬 {platform} <span class="art-muted">{date}</span></div>
  <div class="art-slack-msgs">{"".join(rows)}</div>
</div>'''


def _render_log(el) -> str:
    log_type = _h(_inner_tag(el, 'log_type') or el.get('log_type', 'Log'))
    host     = _inner_tag(el, 'host') or _inner_tag(el, 'facility') or ''
    entries  = _inner_tag(el, 'entries') or _inner_tag(el, 'commands') or _inner(el)
    note     = _inner_tag(el, 'note') or ''
    note_html = f'<div class="art-log-note">ℹ {_h(note)}</div>' if note else ''
    return f'''
<div class="art-terminal">
  <div class="art-term-chrome">
    <span class="art-term-dot r"></span><span class="art-term-dot y"></span><span class="art-term-dot g"></span>
    <span class="art-term-title">{log_type}{(" — " + _h(host)) if host else ""}</span>
  </div>
  <pre class="art-term-body">{_h(entries)}</pre>
  {note_html}
</div>'''


def _render_policy(el) -> str:
    org  = _h(_inner_tag(el, 'org') or _inner_tag(el, 'source') or '')
    did  = _h(_inner_tag(el, 'doc_id') or '')
    date = _h(_inner_tag(el, 'date') or '')
    subj = _h(_inner_tag(el, 'subject') or '')
    body = _h(_inner_tag(el, 'body') or _inner_tag(el, 'text') or '')
    return f'''
<div class="art-document">
  <div class="art-doc-header">
    <div class="art-doc-org">{org}</div>
    <div class="art-doc-meta">{did} &nbsp;·&nbsp; {date}</div>
    <div class="art-doc-subject"><strong>{subj}</strong></div>
  </div>
  <pre class="art-doc-body">{body}</pre>
</div>'''


def _render_social(el) -> str:
    profile_el = el.find('profile')
    msg_el     = el.find('message')
    platform   = _h(_inner_tag(el, 'platform') or 'LinkedIn')

    if profile_el is not None:
        name   = _h(_inner_tag(profile_el, 'display_name'))
        hline  = _h(_inner_tag(profile_el, 'headline'))
        conns  = _h(_inner_tag(profile_el, 'connections'))
        created= _h(_inner_tag(profile_el, 'account_created'))
        emp    = _h(_inner_tag(profile_el, 'employment_history'))
        edu    = _h(_inner_tag(profile_el, 'education'))
        act    = _h(_inner_tag(profile_el, 'activity'))
        profile_html = f'''
<div class="art-social-profile">
  <div class="art-social-avatar">👤</div>
  <div class="art-social-info">
    <div class="art-social-name">{name}</div>
    <div class="art-social-headline">{hline}</div>
    <div class="art-social-meta"><span>🔗 {conns}</span> <span>📅 Created: {created}</span></div>
    <div class="art-social-detail"><strong>Employment:</strong> {emp}</div>
    <div class="art-social-detail"><strong>Education:</strong> {edu}</div>
    <div class="art-social-detail"><strong>Activity:</strong> {act}</div>
  </div>
</div>'''
    else:
        profile_html = ''

    if msg_el is not None:
        frm  = _h(_inner_tag(msg_el, 'from'))
        body = _h(_inner_tag(msg_el, 'body'))
        msg_html = f'<div class="art-social-message"><div class="art-lbl">Message from {frm}:</div><pre class="art-email-body">{body}</pre></div>'
    else:
        msg_html = ''

    return f'<div class="art-social"><div class="art-social-platform">🔗 {platform}</div>{profile_html}{msg_html}</div>'


def _render_transcript(el) -> str:
    date     = _h(_inner_tag(el, 'call_date') or '')
    cid      = _h(_inner_tag(el, 'caller_id_displayed') or '')
    note_raw = _inner_tag(el, 'note') or ''
    lines    = []
    for line in el.findall('.//line'):
        spk  = _h(line.get('speaker', ''))
        text = _h((line.text or '').strip())
        cls  = 'art-call-caller' if 'Caller' in spk else 'art-call-recipient'
        lines.append(f'<div class="art-call-line {cls}"><span class="art-call-spk">{spk}:</span> <span>{text}</span></div>')
    note_html = f'<div class="art-log-note">ℹ {_h(note_raw)}</div>' if note_raw else ''
    return f'''
<div class="art-transcript">
  <div class="art-transcript-hdr">📞 Phone Call — {date}<br><span class="art-muted">Caller ID: {cid}</span></div>
  <div class="art-transcript-body">{"".join(lines)}</div>
  {note_html}
</div>'''


def _render_report_doc(el) -> str:
    rid   = _h(_inner_tag(el, 'report_id') or _inner_tag(el, 'doc_id') or '')
    by    = _h(_inner_tag(el, 'submitted_by') or '')
    date  = _h(_inner_tag(el, 'date_of_incident') or _inner_tag(el, 'date') or '')
    subj  = _h(_inner_tag(el, 'subject') or '')
    narr  = _inner_tag(el, 'narrative') or _inner_tag(el, 'findings') or ''
    conc  = _h(_inner_tag(el, 'conclusion') or '')
    cctv  = _h(_inner_tag(el, 'cctv_footage_available') or '')
    cls   = _h(_inner_tag(el, 'classification') or '')
    return f'''
<div class="art-report-doc">
  <div class="art-report-header">
    {'<div class="art-report-classified">' + cls + '</div>' if cls else ''}
    <div class="art-report-id">{rid}</div>
    {'<div class="art-report-meta">Submitted by: ' + by + '</div>' if by else ''}
    <div class="art-report-meta">Date: {date}</div>
    {'<div class="art-report-subject"><strong>' + subj + '</strong></div>' if subj else ''}
  </div>
  <pre class="art-doc-body">{_h(narr)}</pre>
  {'<div class="art-report-conclusion"><strong>Conclusion:</strong> ' + conc + '</div>' if conc else ''}
  {'<div class="art-report-meta">CCTV: ' + cctv + '</div>' if cctv else ''}
</div>'''


def _render_cert(el) -> str:
    tool   = _h(_inner_tag(el, 'tool') or '')
    url    = _h(_inner_tag(el, 'url') or '')
    proto  = _h(_inner_tag(el, 'tls_version') or _inner_tag(el, 'protocol') or '')
    cipher = _h(_inner_tag(el, 'cipher_suite') or '')
    cert_el= el.find('certificate')
    cert_html = ''
    if cert_el is not None:
        rows = ''.join(
            f'<div><span class="art-lbl">{_h(c.tag.replace("_"," ").title())}:</span> {_h((c.text or "").strip())}</div>'
            for c in cert_el
        )
        cert_html = f'<div class="art-cert-block">{rows}</div>'
    warns = _inner_tag(el, 'warnings') or ''
    return f'''
<div class="art-cert">
  <div class="art-cert-hdr">🔒 Certificate Inspection — {tool}</div>
  <div class="art-cert-url"><code>{url}</code></div>
  <div><span class="art-lbl">Protocol:</span> {proto} &nbsp; <span class="art-lbl">Cipher:</span> {cipher}</div>
  {cert_html}
  <pre class="art-cert-warns art-warn">{_h(warns)}</pre>
</div>'''


def _render_composite(el) -> str:
    parts = ['<div class="art-composite">']
    for comp in el.findall('component') or el.findall('email'):
        cid   = comp.get('id', '')
        ctype = comp.get('type', 'text')
        label_el = comp.find('label')
        label = _h((label_el.text or '').strip()) if label_el is not None else _h(f'Component {cid}')
        # Render the component content based on its type
        inner_html = _render_by_type(ctype, comp)
        parts.append(f'<div class="art-comp-block"><div class="art-comp-label">{label}</div>{inner_html}</div>')
    # Also handle direct email children (email_thread nested in composite)
    parts.append('</div>')
    return ''.join(parts)


def _render_by_type(ctype: str, el) -> str:
    if ctype in ('email', 'email_thread'):
        return _render_email_single(el)
    elif ctype in ('log_file', 'rfid_log', 'pacs_log', 'terminal_output'):
        return _render_log(el)
    elif ctype in ('chat_transcript', 'slack_thread', 'slack'):
        return _render_chat(el)
    elif ctype in ('policy_memo', 'policy_extract'):
        return _render_policy(el)
    elif ctype in ('cert_inspection',):
        return _render_cert(el)
    elif ctype in ('sms',):
        body = _h(_inner_tag(el, 'body') or _inner(el))
        frm  = _h(_inner_tag(el, 'from') or el.get('from', ''))
        ts   = _h(_inner_tag(el, 'timestamp') or '')
        return f'<div class="art-sms"><div class="art-sms-from">{frm} · {ts}</div><div class="art-sms-body">{body}</div></div>'
    elif ctype in ('ascii_floorplan', 'ascii_diagram'):
        diag = _inner_tag(el, 'diagram') or _inner(el)
        leg  = _inner_tag(el, 'legend') or ''
        return f'<pre class="art-ascii">{_h(diag)}</pre>{"<div class=art-log-note>"+_h(leg)+"</div>" if leg else ""}'
    elif ctype in ('found_device', 'incident_report', 'investigation_report'):
        return _render_report_doc(el)
    elif ctype in ('it_analysis',):
        contents = _inner_tag(el, 'contents') or _inner(el)
        analyst  = _h(_inner_tag(el, 'analyst') or '')
        env      = _h(_inner_tag(el, 'environment') or '')
        conc     = _h(_inner_tag(el, 'conclusion') or '')
        return f'''<div class="art-terminal">
  <div class="art-term-chrome"><span class="art-term-dot r"></span><span class="art-term-dot y"></span><span class="art-term-dot g"></span>
  <span class="art-term-title">IT Analysis — {analyst} [{env}]</span></div>
  <pre class="art-term-body">{_h(contents)}</pre>
  {'<div class="art-log-note art-warn">⚠ ' + conc + '</div>' if conc else ''}
</div>'''
    elif ctype in ('visitor_log',):
        log_type = _h(_inner_tag(el, 'log_type') or 'Visitor Log')
        entries  = _inner_tag(el, 'entries') or ''
        note     = _h(_inner_tag(el, 'note') or '')
        return f'<div class="art-terminal"><div class="art-term-chrome"><span class="art-term-dot r"></span><span class="art-term-dot y"></span><span class="art-term-dot g"></span><span class="art-term-title">{log_type}</span></div><pre class="art-term-body">{_h(entries)}</pre>{"<div class=art-log-note>" + note + "</div>" if note else ""}</div>'
    elif ctype in ('calendar_note',):
        src  = _h(_inner_tag(el, 'source') or '')
        text = _h(_inner_tag(el, 'entry') or _inner(el))
        return f'<div class="art-document"><div class="art-doc-header"><div class="art-doc-org">{src}</div></div><pre class="art-doc-body">{text}</pre></div>'
    else:
        return f'<pre class="art-term-body">{_h(_inner(el))}</pre>'


def _render_generic(el) -> str:
    return f'<pre class="art-term-body">{_h(_inner(el))}</pre>'


def _inner_tag(el, tag: str) -> str:
    """Get inner text of a direct child tag."""
    child = el.find(tag)
    if child is None:
        return ''
    return _inner(child)
