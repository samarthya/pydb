import json

class TableConfig:
    """Class to encapsulate the config.json capability"""

    config_file = "config.json"

    def __init__(self, config_file):
        self.config_file = config_file
        with open(config_file,encoding='utf-8') as file:
            self.config_data = json.load(file)

    def get_table_name(self):
        return self.config_data["table_name"]

    def get_columns(self):
        return self.config_data["columns"]

    def get(self, name):
        try:
            return self.config_data[name]
        except KeyError:
            return ""

    def set(self, name, value):
        self.config_data[name]=value

    def overwrite(self):
        with open(self.config_file, 'w', encoding='utf-8') as config_file:
            json.dump(self.config_data, config_file, indent=4)
