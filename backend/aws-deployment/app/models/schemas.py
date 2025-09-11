from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class TaskSchema(BaseModel):
    id: str
    name: str
    description: str
    category: str
    complexity: str
    duration: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)

class ProjectCreate(BaseModel):
    description: str = Field(..., min_length=10, max_length=1000)

class ProjectResponse(BaseModel):
    id: int
    description: str
    tasks: List[TaskSchema]
    total_duration: int
    outputs: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True