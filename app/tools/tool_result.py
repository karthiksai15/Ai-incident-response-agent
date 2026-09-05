from typing import Any

from pydantic import BaseModel


class ToolResult(BaseModel):
    success: bool
    data: Any = None
    error_type: str | None = None
    message: str | None = None
