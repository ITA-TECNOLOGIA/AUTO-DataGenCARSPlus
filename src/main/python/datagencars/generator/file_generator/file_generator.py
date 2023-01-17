from abc import ABC, abstractmethod

from datagencars.generator.file_access.generation_access import GenerationAccess
from datagencars.generator.file_access.item_profile_access import ItemProfileAccess
from datagencars.generator.file_access.schema_access import SchemaAccess
import pandas as pd


class FileGenerator(ABC):

    def __init__(self, generation_file_path, schema_file_path, item_profile_path=None):
        self.generation_access = GenerationAccess(file_path=generation_file_path)   
        if item_profile_path:
            self.item_profile_access = ItemProfileAccess(file_path=item_profile_path)
        self.schema_access = SchemaAccess(file_path=schema_file_path)
        attribute_name_list = self.schema_access.get_attribute_name_list()
        self.file_df = pd.DataFrame(columns=attribute_name_list)

    @abstractmethod
    def generate_file(self):
        pass

