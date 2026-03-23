import json
import logging
import uuid

from config import settings
from db import db

logger = logging.getLogger(__name__)


async def create_audit_log(ticket_id: str, ip: str) -> str:
    audit_id = str(uuid.uuid4())

    query = """
    INSERT INTO audit_log (
        id, location, action, module,
        entity_id, entity_title,
        description, details
    )
    VALUES (
        $1, $2, $3, $4,
        $5, $6,
        $7, $8::jsonb
    )
    RETURNING id;
    """

    row = await db.pool.fetchrow(
        query,
        audit_id,
        settings.DEFAULT_LOCATION,
        "CREATE_TICKET",
        settings.DEFAULT_APP_NAME,
        ticket_id,
        f"FIDS Down {ip}",
        f"Ticket created for FIDS down at {ip}",
        json.dumps({"ip": ip}),
    )

    logger.info("Audit log created: %s for ticket %s", row["id"], ticket_id)
    return row["id"]