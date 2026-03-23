from typing import Any, Optional

from pydantic import BaseModel


class FidsResponse(BaseModel):
    success: bool
    ticket_id: str
    agentic_action_id: Optional[str] = None
    audit_log_id: Optional[str] = None
    external_status: int
    external_response: dict[str, Any] | str