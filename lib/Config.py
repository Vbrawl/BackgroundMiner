



class Config:
    binary_name = "xmrig.exe"
    config_name = "config.json"
    server_address = "http://localhost:8080"

    chunk_size = 1024


    KEY:str = ""
    IV:int = 0



    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)