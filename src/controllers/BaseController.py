from helpers.config import Settings, get_settings 
import os
import secrets
import re
import unicodedata

class BaseController:
    
    def __init__(self):
        self.app_settings = get_settings()
        
        self.base_dir = os.path.dirname(os.path.dirname(__file__))   ## /../../src
        self.files_dir = os.path.join(self.base_dir, "assets/files") ## src/assets/files
        
        
        
    
    def generate_hex_key(self, length: int = 16) -> str:
        return secrets.token_hex(length // 2)
    



    def secure_filename(self,filename: str) -> str:
        filename = filename.strip()
        filename = os.path.basename(filename)

        filename = unicodedata.normalize("NFKD", filename)
        filename = filename.encode("ascii", "ignore").decode("ascii")

        filename = re.sub(r"[^A-Za-z0-9._-]", "_", filename)

        if not filename:
            filename = "file"

        name, ext = os.path.splitext(filename)

        if name.upper() in self.app_settings.WINDOWS_RESERVED:
            name = f"file_{name}"

        filename = (name[:100] + ext[:10])  # limit length

        return filename
    
    def get_database_path(self, db_name: str):
        database_path = os.path.join(self.base_dir, db_name)
        os.makedirs(database_path, exist_ok=True)
        
        return database_path