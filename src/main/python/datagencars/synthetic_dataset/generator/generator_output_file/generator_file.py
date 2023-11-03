from abc import ABC, abstractmethod
import pandas as pd

from datagencars.synthetic_dataset.generator.access_schema.access_generation_config import AccessGenerationConfig
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema


class GeneratorFile(ABC):

    def __init__(self, generation_config, schema):
        self.access_generation_config = None
        if generation_config != None:
            # Access generation config.
            self.access_generation_config = AccessGenerationConfig(file_str=generation_config)
        # Schema access.
        self.schema_access = AccessSchema(file_str=schema)
        # Getting attribute names:
        attribute_name_list = self.schema_access.get_attribute_name_list()
        self.file_df = pd.DataFrame(columns=attribute_name_list)

    @abstractmethod
    def generate_file(self):
        pass
