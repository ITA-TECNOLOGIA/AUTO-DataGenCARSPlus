from datagencars.synthetic_dataset.generator.generator_output_file.generator_context_file import GeneratorContextFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_item_file import GeneratorItemFile


class ReplaceNullValues:

    def __init__(self, file_df):
        self.file_df = file_df        

    def regenerate_item_file(self, item_schema):
        """
        Replacing null values in the schema file: "item.csv".
        :param: The item schema file.
        :return: The item schema file with replace null values.  
        """
        if self.file_df.isna().any().any():
            generation_config = '[dimension] \n'        
            generation_config += 'number_item=' + str(self.file_df.shape[0]) + '\n'            
            generation_config += 'percentage_item_null_value=0' + '\n'
            item_file_generator = GeneratorItemFile(generation_config=generation_config, item_schema=item_schema)
            return item_file_generator.generate_file(self.file_df) 
        else:
            return self.file_df


    def regenerate_context_file(self, context_schema):
        """
        Replacing null values in the schema file: "context.csv".
        :param: The context schema file.
        :return: The context schema file with replace null values.
        """
        if self.file_df.isna().any().any():
            generation_config = '[dimension] \n'        
            generation_config += 'number_context=' + str(self.file_df.shape[0]) + '\n'            
            generation_config += 'percentage_context_null_value=0' + '\n'
            context_file_generator = GeneratorContextFile(generation_config=generation_config, context_schema=context_schema)
            return context_file_generator.generate_file(self.file_df)
        else:
            return self.file_df 
