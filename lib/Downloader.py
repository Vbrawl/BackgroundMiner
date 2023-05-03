import requests
import platform
from lib.TempManager import TempManager


class Downloader:
    NAMESPACE = "/"

    def __init__(self, server_address:str, chunk_size:int):
        self.server_address = server_address
        self.chunk_size = chunk_size

        NAMESPACE_MAP = {
            "WINDOWS": "W",
            "LINUX": "L",
            "DARWIN": "D"
        }

        self.NAMESPACE = f"/{NAMESPACE_MAP[platform.system().upper()]}{platform.architecture()[0][:2]}/"
    
    def download(self, file:str) -> str:
        filepath = TempManager.get_path(file)

        r = requests.get(self.server_address + self.NAMESPACE + file, stream=True, timeout=30, verify=False)
        f = TempManager.open_file(filepath, 'wb')

        for chunk in r.iter_content(self.chunk_size):
            if chunk:
                f.write(chunk)
        
        f.close()
        return filepath