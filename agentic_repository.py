import json
import logging
import uuid
from datetime import datetime

from config import settings
from db import db

logger = logging.getLogger(__name__)


async def create_agentic_action(ticket_id: str, ip: str) -> str:
    action_id = str(uuid.uuid4())
    now = datetime.utcnow()

    details = {
        "target": {
            "ip_address": ip,
            "device_type": "FIDS_DISPLAY"
        },
        "execution": {
            "method": "REMOTE_INSTALL_FILE",
            "script": settings.FIDS_SCRIPT_PATH,
            "timestamp": now.isoformat() + "Z"
        }
    }

    query = """
    INSERT INTO agentic_actions (
        id, location, action_type, description, details,
        status, ticket_id, approved_by, executed_at, result
    )
    VALUES (
        $1, $2, $3, $4, $5::jsonb,
        'executed', $6, 'Auto-Approved', $7, 'Success'
    )
    RETURNING id;
    """

    row = await db.pool.fetchrow(
        query,
        action_id,
        settings.DEFAULT_LOCATION,
        "FIDS_RESTART",
        f"Triggered restart for FIDS IP {ip}",
        json.dumps(details),
        ticket_id,
        now,
    )

    logger.info("Agentic action created: %s for ticket %s", row["id"], ticket_id)
    return row["id"]