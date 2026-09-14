import json,sqlite3,threading
from pathlib import Path
from niriksh_edge.models import ObservationEvent
class EventBuffer:
    """SQLite metadata-only outbox. The schema has no frame/blob column."""
    def __init__(self,path='edge_events.db'):
        self.path=Path(path);self.lock=threading.Lock()
        with self._db() as db:db.execute('CREATE TABLE IF NOT EXISTS events(event_id TEXT PRIMARY KEY, body TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)')
    def _db(self):return sqlite3.connect(self.path)
    def add(self,event:ObservationEvent):
        with self.lock,self._db() as db:db.execute('INSERT OR IGNORE INTO events(event_id,body) VALUES (?,?)',(event.event_id,json.dumps(event.as_dict())))
    def pending(self,limit=100):
        with self.lock,self._db() as db:return [(r[0],json.loads(r[1])) for r in db.execute('SELECT event_id,body FROM events ORDER BY created_at LIMIT ?',(limit,))]
    def remove(self,event_id):
        with self.lock,self._db() as db:db.execute('DELETE FROM events WHERE event_id=?',(event_id,))
    def count(self):
        with self._db() as db:return db.execute('SELECT COUNT(*) FROM events').fetchone()[0]
