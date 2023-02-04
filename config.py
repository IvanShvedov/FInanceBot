import yaml
import os


class Config:

    _instance = None

    __slots__ = [
        '_path',
        'API_TOKEN',
        'DATABASE_NAME'
    ]

    def __init__(self, yaml_file: str):
        self._path = yaml_file
        self._read()

    def __call__(cls, *args, **kwargs):
        if cls is not cls._instance:
            instance = super().__call__(*args, **kwargs)
            cls._instance = instance
        return cls._instance
        
    def to_dict(self):
        return {field.lower(): getattr(self, field) for field in self.__slots__}

    def _read(self):
        if not os.path.exists(self._path):
            raise AttributeError(f"Config yaml doesnot exist: {self._path}")

        with open(self._path) as config_file:
            config_content = config_file.read()
            config_yaml = yaml.safe_load(config_content)

        for k, v in config_yaml.items():
            k = k.upper()
            if k in self.__slots__:
                setattr(self, k, v)