import json
import logging
import uuid

from config import settings
from db import db

logger = logging.getLogger(__name__)


async def create_agentic_action(ticket_id: str, ip: str) -> str:
    action_id = str(uuid.uuid4())

    query = """
    INSERT INTO agentic_actions (
        id, location, action_type, description, details,
        status, ticket_id, approved_by
    )
    VALUES (
        $1, $2, $3, $4, $5::jsonb,
        'approved', $6, 'System'
    )
    RETURNING id;
    """

    row = await db.pool.fetchrow(
        query,
        action_id,
        settings.DEFAULT_LOCATION,
        "FIDS_RESTART",
        f"Triggered restart for FIDS IP {ip}",
        json.dumps({"ip": ip}),
        ticket_id,
    )

    logger.info("Agentic action created: %s for ticket %s", row["id"], ticket_id)
    return row["id"]