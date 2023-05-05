import pandas as pd
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_output_file.generator_context import GeneratorContextFile


class ReplaceNullValues:

    def __init__(self, file_df):
        self.file_df = file_df

    def regenerate_item_file(self, item_schema, item_profile=None, with_correlation=False):
        '''
            Generating file: item.csv
        '''        
        pass
        #item_file_generator = GeneratorItemFile(self.generation_config, item_schema, item_profile)
        #return item_file_generator.generate_file(with_correlation)        

    def regenerate_context_file(self, context_schema):
        '''
            Generating file (for CARS): context.csv
        '''        
        context_file_generator = GeneratorContextFile(context_schema)
        return context_file_generator.generate_file(self.file_df)