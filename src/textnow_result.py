from __future__ import annotations

from dataclasses import dataclass
from typing import Any

@dataclass
class TextNowResult:
    """
    Return envelope for Textnow-server API requests
    """
    result: Any
    error_code: Any
    message: str
