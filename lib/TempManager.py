import tempfile, os
from typing import IO



class TempManager:
    TEMPDIR = tempfile.mkdtemp()

    @staticmethod
    def get_path(filename:str) -> str:
        return os.path.join(TempManager.TEMPDIR, filename)

    @staticmethod
    def open_file(filename:str, mode = 'r') -> IO:
        return open(filename, mode)