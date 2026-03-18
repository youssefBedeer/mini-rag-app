from enum import Enum 

class ResponseSignal(Enum):
    
    FILE_VALIDATION_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEED = "file_size_exceed" 
    FILE_UPLOAD_SUCCESS = "file_upload_success" 
    FILE_UPLOAD_FAILED = "file_upload_failed"
    FILES_NOT_FOUND = "files_not_found"
    FILE_ID_ERROR = "no_file_with_this_id"
    PROCESS_SUCCESS = "processing_done." 
    PROCESS_FAILED = "processing_failed."
    