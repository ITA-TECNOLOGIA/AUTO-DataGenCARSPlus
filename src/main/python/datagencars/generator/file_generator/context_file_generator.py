import logging

from datagencars.generator.file_generator.file_generator import FileGenerator
from datagencars.generator.instance_generator.instance_gaussian_generator import InstanceGaussianGenerator
from datagencars.generator.instance_generator.instance_random_generator import InstanceRandomGenerator


class ContextFileGenerator(FileGenerator):
    '''
    Generator of the context file (context.csv), by using configuration files. 
    The resulting file contains information related to contexts (e.g., context_id, transport_way, mobility, weekday, mood, companion, time_of_day, distance, etc.).
    The following files are required: generation_config.conf and context_schema.conf.  
    '''

    def __init__(self, generation_file_path, context_schema_file_path):
        super().__init__(generation_file_path, context_schema_file_path)        

    def generate_file(self):
        '''
        Generates the context file.        
        :return: A dataframe with context information.         
        '''
        instance_generator = None
        if self.generation_access.is_gaussian_distribution():
            # Gaussian distribution:
            instance_generator = InstanceGaussianGenerator(generation_access=self.generation_access, schema_access=self.schema_access)
        else:
            # Random without correlation:
            instance_generator = InstanceRandomGenerator(generation_access=self.generation_access, schema_access=self.schema_access)
        
        # Number of contexts to be generated.
        number_context = self.generation_access.get_number_context()
        for _ in range(number_context):
            attribute_list = instance_generator.generate_instance()
            self.file_df.loc[len(self.file_df.index)] = attribute_list

        # Adding context_id column:
        context_id_list = list(range(1, number_context+1))
        self.file_df.insert(loc=0, column='context_id', value=context_id_list)
        return self.file_df.copy()


# generation_file_path = 'resources/data/generation_config.conf'
# context_schema_file_path = 'resources/data/context_schema.conf'
# context_file_generator = ContextFileGenerator(generation_file_path, context_schema_file_path)
# context_file_df = context_file_generator.generate_file()
# print(context_file_df)