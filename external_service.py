import logging

import httpx

from config import settings

logger = logging.getLogger(__name__)


async def call_fids_deploy(ip: str) -> tuple[int, dict]:
    """Trigger FIDS install-file deploy for the given IP."""

    params = {
        "scriptPath": settings.FIDS_SCRIPT_PATH,
        "ip": ip,
        "username": settings.FIDS_DEVICE_USERNAME,
        "password": settings.FIDS_DEVICE_PASSWORD,
        "logFilePath": settings.FIDS_LOG_FILE_PATH,
        "remotePath": settings.FIDS_REMOTE_PATH,
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {settings.FIDS_AUTH_TOKEN}",
        "Content-Type": "application/json",
    }

    logger.info("Calling FIDS deploy for IP %s", ip)

    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.post(
            settings.FIDS_DEPLOY_URL,
            params=params,
            headers=headers,
        )

    logger.info("FIDS deploy response: status=%d", res.status_code)
    return res.status_code, res.json()