import logging

from datagencars.synthetic_dataset.generator.generator_output_file.generator_user import GeneratorUserFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_item import GeneratorItemFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_context import GeneratorContextFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_rating import GeneratorRatingFile


class GenerateSyntheticDataset:
    '''
    Generate a synthetic dataset.
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
        
    def generate_rating_file(self, user_df, user_profile_df, item_df, item_schema, with_context=False, context_df=None, context_schema=None):
        '''
            Generating file: rating.csv
        '''
        rating_file_generator = GeneratorRatingFile(self.generation_config, user_df, user_profile_df, item_df, item_schema, context_df, context_schema)          
        return rating_file_generator.generate_file(with_context)    
