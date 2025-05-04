from flask import session
from datetime import date

MAX_RECENTS = 5

def get_recents():
    return session.get('recent_searches', [])

def add_recent(entry: dict):
    recents = session.get('recent_searches', [])

    recents = [r for r in recents if not (
        r['ticker'] == entry['ticker']
        and r['start']  == entry['start']
        and r['end']    == entry['end']
        and str(r['ma_window']) == str(entry['ma_window'])
    )]

    recents.insert(0, entry)
    recents = recents[:MAX_RECENTS]

    session['recent_searches'] = recents
    session.modified = True
