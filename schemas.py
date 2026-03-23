from typing import Any

from pydantic import BaseModel


class FidsResponse(BaseModel):
    success: bool
    ticket_id: str
    agentic_action_id: str
    audit_log_id: str
    external_status: int
    external_response: dict[str, Any]