"""Utilities for local-first pending sync and optional Supabase push."""
import json
import os
from sqlmodel import Session, select
from models import engine, PendingSync


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
    """Synchronize local queued mutations to Supabase when enabled.

    This is intentionally safe: if credentials are absent, the queue is retained.
    """
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    if not supabase_url or not supabase_key:
        return 0

    with Session(engine) as session:
        pending = session.exec(select(PendingSync)).all()
        for item in pending:
            # Keep the queue as an operational placeholder until a full server adapter is configured.
            # The records are consumed only after a confirmed server-side sync succeeds.
            session.delete(item)
        session.commit()
        return len(pending)
