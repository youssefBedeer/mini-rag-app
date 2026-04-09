from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ResponseSignal

import os
from pathlib import Path
from fastapi import UploadFile

class DataController(BaseController): 
    def __init__(self):
        super().__init__()
        
        self.size_scale = 1048576 # to convert MB to bytes
        
    
    def validate_file_type(self, file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEED.value
        
        return True, ResponseSignal.FILE_UPLOAD_SUCCESS.value
    
    
    def generate_unique_file_name(self, original_file_name:str, project_id:str): # RandomKey_id_fname
        random_key = BaseController().generate_hex_key()        
        clean_filename = BaseController().secure_filename(filename=original_file_name)
        new_filename = str(Path(f"{random_key}_{clean_filename}"))
        return new_filename