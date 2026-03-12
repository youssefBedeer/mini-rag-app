from fastapi import APIRouter, Request, Depends
from models.ProjectModel import ProjectModel
from pymongo.database import Database

test_router = APIRouter(
    prefix="/test",
    tags=["test"]
)
def get_db(request: Request)->Database:
    return request.app.db_client

@test_router.post("/{project_id}")
async def test(project_id: str, db:Database=Depends(get_db)):
    project_model = ProjectModel(db_client=db)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    return {"project_id": project_id,"project": project}


@test_router.get("/mongo/getall")
async def get_all_projects(db:Database=Depends(get_db)):
    project_model= ProjectModel(db_client=db)
    all_projects = await project_model.get_all_projects()
    return all_projects