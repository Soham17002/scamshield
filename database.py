import sqlite3, os
from datetime import datetime
DB=os.path.join(os.path.dirname(__file__),'scamshield.db')
def connect():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
    with connect() as c: c.execute('''CREATE TABLE IF NOT EXISTS scans(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT NOT NULL,scan_type TEXT NOT NULL,input_summary TEXT NOT NULL,risk_score INTEGER NOT NULL,result TEXT NOT NULL,indicators TEXT NOT NULL)''')
def add_scan(kind,source,score,level,summary,indicators):
    raw=' '.join((source or '').split())
    if kind in ('Message', 'Email'):
        clean=f'{kind} scan · {len(raw)} characters'
    elif kind=='URL':
        # Keep history useful without retaining query strings or fragments.
        from urllib.parse import urlparse
        candidate=raw if '://' in raw else 'http://'+raw
        try:
            parsed=urlparse(candidate)
            clean=(parsed.hostname or 'URL scan') + (parsed.path[:60] if parsed.path and parsed.path != '/' else '')
        except Exception:
            clean='URL scan'
    else:
        clean=raw[:120]
    with connect() as c: c.execute('INSERT INTO scans(created_at,scan_type,input_summary,risk_score,result,indicators) VALUES(?,?,?,?,?,?)',(datetime.now().isoformat(timespec='seconds'),kind,clean,int(score),level,'; '.join(indicators)))
def get_scans(limit=100):
    with connect() as c: return [dict(r) for r in c.execute('SELECT * FROM scans ORDER BY id DESC LIMIT ?', (limit,)).fetchall()]
def delete_scan(scan_id):
    with connect() as c: c.execute('DELETE FROM scans WHERE id=?',(int(scan_id),))
def clear_scans():
    with connect() as c: c.execute('DELETE FROM scans')
def stats():
    rows=get_scans(100000); return {'total':len(rows),'high':sum(r['result']=='High Risk' for r in rows),'medium':sum(r['result']=='Medium Risk' for r in rows),'low':sum(r['result']=='Low Risk' for r in rows)}
