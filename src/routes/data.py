from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os 
from helpers.config import Settings, get_settings
from controllers import DataController, ProjectController, ProcessController
import aiofiles
from models import ResponseSignal
import logging 
from .schemas.data import ProcessRequest
from models import ChunkModel, AssetModel, ProjectModel
from models import Project, DataChunk, Asset
from models.enums import AssetTypeEnums
from pymongo.database import Database


logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix= "/api/v1/data",
    tags = ["api_v1", "data"]
)

def get_db(request:Request)->Database:
    return request.app.db_client


@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str, file:UploadFile,
                    app_settings:Settings = Depends(get_settings),
                    db:Database=Depends(get_db)):
    
    data_controller = DataController()
    project_controller = ProjectController()
    project_model = await ProjectModel.create_instance(db_client=db)
    asset_model = await AssetModel.create_instance(db_client=db)
    
    # validate the file properties
    is_valid, result_signal = data_controller.validate_file_type(file=file)
    
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"signal" : result_signal})
        
    # store in mongodb    
    project = await project_model.get_project_or_create_one(project_id=project_id)
        
        
    ## store file in a folder with the name of project_id
    project_project_path = project_controller.get_project_path(project_id=project_id) #src/assets/files/id
    file_id = data_controller.generate_unique_file_name(original_file_name=file.filename,
                                                        project_id=project_id)
    file_path = os.path.join(project_project_path, file_id)
    
    # open file writing as binary , chunk by chunk -> memory efficient
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        
        logger.error(f"Error while uploading file: {e}")
        
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content= ResponseSignal.FILE_UPLOAD_FAILED.value
        )
        
    # store asset info in (asset_collection) db
    asset_size = round(os.path.getsize(file_path) / 1024, 2)
    asset_resource = Asset(
                        asset_name=file_id, 
                        asset_project_id=project.id,
                        asset_size=asset_size,
                        asset_type=AssetTypeEnums.FILE.value)
    
    asset_record = await asset_model.create_asset(asset=asset_resource)

    return JSONResponse(
            content={
                "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                "file_id": str(asset_record.id),
            }
        )
        
    
@data_router.post("process/{project_id}")
async def process_data(project_id: str, process_request: ProcessRequest,
                    db:Database=Depends(get_db)):
    
    chunk_size = process_request.chunk_size 
    overlap = process_request.overlap 
    do_reset = process_request.do_reset
    
    
    project_model = await ProjectModel.create_instance(db_client=db)
    chunk_model = await ChunkModel.create_instance(db_client=db)
    asset_model = await AssetModel.create_instance(db_client=db)
    process_controller = ProcessController(project_id=project_id)
    
    project = await project_model.get_project_or_create_one(project_id=project_id)
    
    if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )
        
    project_assets_ids = {}
    if process_request.file_id:
        asset_record = await asset_model.get_asset_record(
            asset_project_id= project.id,
            asset_name= process_request.file_id
        )
        
        if asset_record is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"signal": ResponseSignal.FILE_ID_ERROR.value})        
            
        project_assets_ids = {asset_record.id: asset_record.asset_name}
    else:
        project_assets = await asset_model.get_all_project_assets(
            asset_project_id=project.id,
            asset_type=AssetTypeEnums.FILE.value
        )
        
        project_assets_ids = {
            record.id: record.asset_name 
            for record in project_assets
        }

        # check if there is no files 
        if not project_assets_ids:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"signal": ResponseSignal.FILES_NOT_FOUND.value})
        
        
    no_records = 0 
    no_files = 0    
    for asset_id, file_id in project_assets_ids.items():
        
        file_content = process_controller.get_content(file_id=file_id)

        if file_content is None:
            logger.error(f"Error while processing file: {file_id}")
            continue
        
        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            file_id=file_id, 
            chunk_size=chunk_size,
            overlap=overlap
        )
        if file_chunks is None or len(file_chunks) == 0:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={
                                    "signal" : ResponseSignal.PROCESS_FAILED.value
                                })
            
        file_chunks_records = [
            DataChunk(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i+1,
                chunk_project_id= project.id,
                chunk_asset_id=asset_id
                
            )

            for i, chunk in enumerate(file_chunks)
        ]
        


        no_records += await chunk_model.insert_many_chunks(chunks=file_chunks_records)
        no_files += 1

    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESS_SUCCESS.value,
            "inserted_chunks": no_records,
            "processed_files": no_files
        }
    )
    
