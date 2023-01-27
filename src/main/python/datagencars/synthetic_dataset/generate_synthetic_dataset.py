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
    
    def generate_item_file(self, item_schema):
        '''
            Generating file: item.csv
        '''        
        item_file_generator = GeneratorItemFile(self.generation_config, item_schema)
        return item_file_generator.generate_file()        

    def generate_context_file(self, context_schema):
        '''
            Generating file (for CARS): context.csv
        '''        
        context_file_generator = GeneratorContextFile(self.generation_config, context_schema)
        return context_file_generator.generate_file()
        
    def generate_rating_file(self):
        '''
            Generating file: rating.csv
        '''
        # self.generation_config
        return None


#     def generate_synthetic_dataset(self, with_context, generation_file_path, user_schema_file_path, item_schema_file_path, context_schema_file_path=None):
#         # Generating file: user.csv
#         user_file_generator = UserFileGenerator(generation_file_path, user_schema_file_path)
#         user_file_df = user_file_generator.generate_file()
#         # Generating file: item.csv
#         item_file_generator = ItemFileGenerator(generation_file_path, item_schema_file_path)
#         item_file_df = item_file_generator.generate_file()
#         # Generating file (for CARS): context.csv
#         if with_context:
#             context_file_generator = ContextFileGenerator(generation_file_path, context_schema_file_path)
#             context_file_df = context_file_generator.generate_file()

#         # Generating file: rating.csv
#         rating_file_df = None
#         return user_file_df, item_file_df, context_file_df, rating_file_df


# generator = GenerateSyntheticDataset()

# with_context = True
# ROOT = 'resources/data/'
# generation_file_path = f'{ROOT}generation_config.conf'
# user_schema_file_path = f'{ROOT}user_schema.conf'
# item_schema_file_path = f'{ROOT}item_schema.conf'
# context_schema_file_path = f'{ROOT}context_schema.conf'
# generator.generate_synthetic_dataset(with_context, generation_file_path, user_schema_file_path, item_schema_file_path, context_schema_file_path)