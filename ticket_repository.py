import json
import logging
import uuid
from datetime import datetime, timedelta, timezone

from config import settings
from db import db

logger = logging.getLogger(__name__)


async def create_ticket(ip: str) -> str:
    ticket_id = str(uuid.uuid4())
    now = datetime.utcnow()

    query = """
    INSERT INTO tickets (
        id, title, description, severity, location, status,
        app_name, error_type, assignee,
        sla_deadline, created_at, updated_at, last_seen,
        report_json, instances
    )
    VALUES (
        $1, $2, $3, 'critical', $4, 'open',
        $5, $6, $7,
        $8, $9, $9, $9,
        $10::jsonb, $11::jsonb
    )
    RETURNING id;
    """

    row = await db.pool.fetchrow(
        query,
        ticket_id,
        f"FID Down - {ip}",
        f"FIDS display is down for IP {ip}",
        settings.DEFAULT_LOCATION,
        settings.DEFAULT_APP_NAME,
        settings.DEFAULT_ERROR_TYPE,
        settings.DEFAULT_ASSIGNEE,
        now + timedelta(hours=1),
        now,
        json.dumps({"ip": ip}),
        json.dumps([ip]),
    )

    logger.info("Ticket created: %s for IP %s", row["id"], ip)
    return row["id"]