from datagencars.synthetic_dataset.generator.generator_output_file.generator_context import GeneratorContextFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_item import GeneratorItemFile


class ReplaceNullValues:

    def __init__(self, file_df):
        self.file_df = file_df

    def regenerate_item_file(self, item_schema):
        """
        Replacing null values in the schema file: "item.csv".
        :param: The item schema file.
        :return: The item schema file with replace null values.  
        """
        item_file_generator = GeneratorItemFile(item_schema)
        return item_file_generator.generate_file(False, self.file_df)        

    def regenerate_context_file(self, context_schema):
        """
        Replacing null values in the schema file: "context.csv".
        :param: The context schema file.
        :return: The context schema file with replace null values.
        """        
        context_file_generator = GeneratorContextFile(context_schema)
        return context_file_generator.generate_file(self.file_df)
