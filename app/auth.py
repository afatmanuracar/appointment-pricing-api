import os
from typing import Optional

from fastapi import Header, HTTPException

API_KEY = os.getenv("API_KEY", "dev-secret-key")

async def require_api_key(x_api_key: Optional[str] = Header(default=None)) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
