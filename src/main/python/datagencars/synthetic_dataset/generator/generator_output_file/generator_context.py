from datagencars.synthetic_dataset.generator.generator_instance.generator_instance import GeneratorInstance
from datagencars.synthetic_dataset.generator.generator_output_file.generator_file import GeneratorFile


class GeneratorContextFile(GeneratorFile):
    '''
    Generator of the context file (context.csv), by using configuration files. 
    The resulting file contains information related to contexts (e.g., context_id, transport_way, mobility, weekday, mood, companion, time_of_day, distance, etc.).
    The following files are required: generation_config.conf and context_schema.conf.  
    '''

    def __init__(self, context_schema, generation_config=None):
        super().__init__(generation_config, context_schema)

    def generate_file(self, input_csv=None):
        '''
        Generates the context file.        
        :return: A dataframe with context information.         
        '''
        # Instance generator.
        instance_generator = GeneratorInstance(schema_access=self.schema_access)        
        
        if self.access_generation_config != None:
            # Number of contexts to be generated.
            number_context = self.access_generation_config.get_number_context()
        else:
            number_context = len(input_csv)
        print(f'Total of contexts to generate: {number_context}')
        print('Generating instances by context.')  
        for i in range(number_context):
            if not(input_csv is None):
                instance = input_csv.iloc[i]
            else:
                instance = None
            attribute_list = instance_generator.generate_instance(instance=instance)
            self.file_df.loc[len(self.file_df.index)] = attribute_list

        # Adding context_id column:
        context_id_list = list(range(1, number_context+1))
        self.file_df.insert(loc=0, column='context_id', value=context_id_list)
        
        return self.file_df.copy()
