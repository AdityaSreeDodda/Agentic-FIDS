import logging

from agentic_repository import create_agentic_action
from audit_repository import create_audit_log
from config import settings
from external_service import call_fids_deploy
from ticket_repository import create_ticket
from validators import validate_ip

logger = logging.getLogger(__name__)


async def handle_fids_down(ip: str) -> dict:
    ip = validate_ip(ip)

    if ip not in settings.allowed_ips:
        raise ValueError(f"IP {ip} is not in the allowed list")

    logger.info("Handling FIDS down for IP %s", ip)

    status_code, response = await call_fids_deploy(ip)

    ticket_id = await create_ticket(ip)
    action_id = await create_agentic_action(ticket_id, ip)
    audit_id = await create_audit_log(ticket_id, ip)

    logger.info("FIDS down handled — ticket=%s, action=%s, audit=%s", ticket_id, action_id, audit_id)

    return {
        "ticket_id": ticket_id,
        "agentic_action_id": action_id,
        "audit_log_id": audit_id,
        "external_status": status_code,
        "external_response": response,
    }