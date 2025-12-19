from dataclasses import dataclass
from datetime import datetime


@dataclass
class Lead:
    id: int
    name: str | None = None
    phone: str | None = None
    created_at: datetime | None = None
    consultation: bool = False
