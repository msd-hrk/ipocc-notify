import json

class Config:
    def __init__(self):
        config_path = "app_info/config.json"
        config = json.load(open(config_path, "r"))
        self.srcaddr = config["srcaddr"]
        self.password = config["password"]
        self.desaddr_arry = config["desaddr_arry"]
        self.mongo_url = config["mongo_url"]
