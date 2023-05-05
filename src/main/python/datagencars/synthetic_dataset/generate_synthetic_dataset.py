import logging
from abc import ABC, abstractmethod

from datagencars.synthetic_dataset.generator.generator_output_file.generator_user import GeneratorUserFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_item import GeneratorItemFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_context import GeneratorContextFile


class GenerateSyntheticDataset(ABC):
    '''
    Generates a synthetic dataset.

    Input:    
        [GC] generation_config.conf    
        [US] user_schema.conf
        [UP] user_profile.csv
        [U]  user.csv    
        [IS] item_schema.conf
        [IP] item_profile.conf
        [I]  item.csv
        [CS] context_schema.conf <optional>
        [C]  context.csv <optional>
        [R]  rating.csv

    Algorithm:
        1- acces_schema: Access to schema information.
        2- generator_attribute: Generate attributes, by using acces_schema.
        3- generator_instance: Generate instances, by using generator_attribute.
        4- generator_output_file: Generate user, item, context <optional>, rating files, by using generator_instance.
        5- generate_synthetic_dataset: Generate all output files, by using generator_output_file.

    Output:
        [U]  user.csv   
        [I]  item.csv
        [C]  context.csv <optional>
        [R]  rating.csv
    '''    

    def __init__(self, generation_config):
        self.generation_config = generation_config

    def generate_user_file(self, user_schema):
        '''
            Generating file: user.csv
        '''        
        user_file_generator = GeneratorUserFile(self.generation_config, user_schema)
        return user_file_generator.generate_file()
    
    def generate_item_file(self, item_schema, item_profile=None, with_correlation=False):
        '''
            Generating file: item.csv
        '''        
        item_file_generator = GeneratorItemFile(self.generation_config, item_schema, item_profile)
        return item_file_generator.generate_file(with_correlation)        

    def generate_context_file(self, context_schema):
        '''
            Generating file (for CARS): context.csv
        '''        
        context_file_generator = GeneratorContextFile(self.generation_config, context_schema)
        return context_file_generator.generate_file()
    
    @abstractmethod   
    def generate_rating_file(self, user_df, user_profile_df, item_df, item_schema, with_context=False, context_df=None, context_schema=None):
        '''
            Generating file: rating.csv
        '''
        pass