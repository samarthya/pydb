import json

class TableConfig:
    def __init__(self, config_file):
        with open(config_file,encoding='utf-8') as file:
            self.config_data = json.load(file)

    def get_table_name(self):
        return self.config_data["table_name"]

    def get_columns(self):
        return self.config_data["columns"]
