from datagencars.generator.file_generator.user_file_generator import UserFileGenerator
from datagencars.generator.file_generator.item_file_generator import ItemFileGenerator
from datagencars.generator.file_generator.context_file_generator import ContextFileGenerator


class GenerateSyntheticDataset:
    '''

    '''    

    def __init__(self):
        pass

    def generate_synthetic_dataset(self, with_context, generation_file_path, user_schema_file_path, item_schema_file_path, context_schema_file_path=None):
        # Generating file: user.csv
        user_file_generator = UserFileGenerator(generation_file_path, user_schema_file_path)
        user_file_df = user_file_generator.generate_file()
        # Generating file: item.csv
        item_file_generator = ItemFileGenerator(generation_file_path, item_schema_file_path)
        item_file_df = item_file_generator.generate_file()
        # Generating file (for CARS): context.csv
        if with_context:
            context_file_generator = ContextFileGenerator(generation_file_path, context_schema_file_path)
            context_file_df = context_file_generator.generate_file()

        # Generating file: rating.csv
        rating_file_df = None
        return user_file_df, item_file_df, context_file_df, rating_file_df


generator = GenerateSyntheticDataset()

with_context = True
ROOT = 'resources/data/'
generation_file_path = f'{ROOT}generation_config.conf'
user_schema_file_path = f'{ROOT}user_schema.conf'
item_schema_file_path = f'{ROOT}item_schema.conf'
context_schema_file_path = f'{ROOT}context_schema.conf'
generator.generate_synthetic_dataset(with_context, generation_file_path, user_schema_file_path, item_schema_file_path, context_schema_file_path)