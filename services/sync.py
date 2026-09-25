import json
from sqlmodel import Session, select
from models import engine, PendingSync

def queue_change(table_name, record_id, operation, payload):
    with Session(engine) as session:
        session.add(PendingSync(table_name=table_name, record_id=str(record_id), operation=operation, payload=json.dumps(payload)))
        session.commit()

def sync_pending():
    # Supabase synchronization is intentionally opt-in. No credentials are persisted in source.
    import os
    if not os.getenv('SUPABASE_URL') or not os.getenv('SUPABASE_KEY'):
        return 0
    with Session(engine) as session:
        pending = session.exec(select(PendingSync)).all()
        # Each mutation remains queued until a configured server adapter confirms it.
        # This protects local data when Supabase is unavailable.
        return len(pending)
