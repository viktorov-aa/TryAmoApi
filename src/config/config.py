from dataclasses import dataclass
from pathlib import Path

from dataclasses_json import DataClassJsonMixin
from yamldataclassconfig import create_file_path_field
from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class AmoConfig(DataClassJsonMixin):
    integration_id: str = None
    secret_key: str = None
    base_url: str = None


@dataclass
class DatabaseConfig(DataClassJsonMixin):
    file_name: str = None


@dataclass
class Config(YamlDataClassConfig):
    amo: AmoConfig = None
    database: DatabaseConfig = None

    FILE_PATH: Path = create_file_path_field(Path(__file__).parent / 'config.yaml')


if __name__ == '__main__':
    config = Config()
    config.load()
    print(config.amo.integration_id)
    print(config.amo.secret_key)
    print(config.amo.base_url)
    print(config.database.file_name)
