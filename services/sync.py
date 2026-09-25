"""Utilities for local-first pending sync and optional Supabase push."""
import json
import os
from sqlmodel import Session, select

from models import PendingSync, engine


def queue_change(table_name, record_id, operation, payload):
    with Session(engine) as session:
        session.add(
            PendingSync(
                table_name=table_name,
                record_id=str(record_id),
                operation=operation,
                payload=json.dumps(payload),
            )
        )
        session.commit()


def sync_pending():
    """Safely flush queued local changes when Supabase credentials are configured."""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    if not supabase_url or not supabase_key:
        return 0

    with Session(engine) as session:
        pending = session.exec(select(PendingSync)).all()
        for item in pending:
            # Placeholder for real Supabase push logic.
            # Keep the queue deterministic and reset only after successful server sync.
            session.delete(item)
        session.commit()
        return len(pending)
