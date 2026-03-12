from dataclasses import field, dataclass
from datetime import datetime, UTC
from uuid import uuid4, UUID


@dataclass(slots=True, kw_only=True)
class BaseEntity:
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))

    def __eq__(self, other):
        return self.id == other.id
