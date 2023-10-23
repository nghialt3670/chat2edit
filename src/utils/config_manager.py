import yaml


class ConfigManager:
    def __init__(self, file_path: str):
        self.configs = {}
        self.load_configsuration(file_path)

    def load_configsuration(self, file_path: str) -> None:
        if file_path.endswith('.txt'):
            self.load_txt_configs(file_path)
        elif file_path.endswith('.yaml'):
            self.load_yaml_configs(file_path)
        elif file_path.endswith('.py'):
            self.load_py_configs(file_path)
        else:
            raise ValueError("Unsupported configuration file format")

    def load_txt_configs(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                self.configs[key.strip()] = value.strip()

    def load_yaml_configs(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            self.configs = yaml.safe_load(file)

    def load_py_configs(self, file_path: str) -> None:
        configs = {}
        with open(file_path, 'r') as file:
            exec(file.read(), configs)
        self.configs = configs

    def get(self, key: str):
        return self.configs.get(key, None)