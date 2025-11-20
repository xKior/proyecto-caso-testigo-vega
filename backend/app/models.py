from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: Optional[int]
    title: str
    description: Optional[str]
    status: str
    priority: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }