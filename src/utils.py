import yaml

CONFIG = yaml.safe_load(open("config.yml"))


class Freezable:
    def freeze(self) -> dict:
        return vars(self)
