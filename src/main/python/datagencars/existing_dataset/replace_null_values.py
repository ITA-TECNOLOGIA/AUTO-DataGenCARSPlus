from datagencars.synthetic_dataset.generator.generator_output_file.generator_context import GeneratorContextFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_item import GeneratorItemFile

class ReplaceNullValues:

    def __init__(self, file_df):
        self.file_df = file_df

    def regenerate_item_file(self, item_schema):
        '''
            Generating file: item.csv
        '''        
        item_file_generator = GeneratorItemFile(item_schema)
        return item_file_generator.generate_file(False, self.file_df)        

    def regenerate_context_file(self, context_schema):
        '''
            Generating file (for CARS): context.csv
        '''        
        context_file_generator = GeneratorContextFile(context_schema)
        return context_file_generator.generate_file(self.file_df)