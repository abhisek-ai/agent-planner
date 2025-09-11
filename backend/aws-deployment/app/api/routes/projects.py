from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
import json
import traceback  # Add this
from app.core.database import get_db
from app.models.schemas import ProjectCreate, ProjectResponse
from app.models.models import Project
from app.services.orchestrator import Orchestrator

router = APIRouter()

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new project plan"""
    try:
        # Run the orchestrator
        orchestrator = Orchestrator()
        result = await orchestrator.run(project.description)
        
        # Print result for debugging
        print("Orchestrator result keys:", result.keys())
        print("Number of tasks:", len(result.get('tasks', [])))
        
        # Save to database
        db_project = Project(
            description=project.description,
            tasks=json.dumps(result.get('tasks', [])),
            total_duration=result.get('total_duration', 0)
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        # Return response
        return ProjectResponse(
            id=db_project.id,
            description=db_project.description,
            tasks=result.get('tasks', []),
            total_duration=result.get('total_duration', 0),
            outputs=result.get('outputs', {}),
            created_at=db_project.created_at
        )
        
    except Exception as e:
        print(f"Error in create_project: {type(e).__name__}: {str(e)}")
        print(traceback.format_exc())  # Full error trace
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test")
async def test_endpoint():
    """Test endpoint"""
    return {"status": "ok", "message": "Projects endpoint working"}