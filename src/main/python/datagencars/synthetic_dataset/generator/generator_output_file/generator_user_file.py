from datagencars.synthetic_dataset.generator.generator_instance.generator_instance import GeneratorInstance
from datagencars.synthetic_dataset.generator.generator_output_file.generator_file import GeneratorFile
import streamlit as st
import time


class GeneratorUserFile(GeneratorFile):
    '''
    Generator of the user file (user.csv), by using configuration files. 
    The resulting file contains information related to users (e.g., user_id, age, gender, occupation, birthdate, etc.).  
    The following files are required: generation_config.conf and user_schema.conf.  
    '''

    def __init__(self, generation_config, user_schema):
        super().__init__(generation_config, user_schema)

    def generate_file(self):
        '''
        Generates the user file. 
        :return: A dataframe with user information.         
        '''
        # Instance generator.
        instance_generator = GeneratorInstance(schema_access=self.schema_access)
        # Number of users to be generated.
        number_user = self.access_generation_config.get_number_user()
        print(f'Total of users to generate: {number_user}')
        print('Generating instances by user.')
        number_attributes = self.schema_access.get_number_attributes()
        if number_attributes!=None and number_attributes>0:
            # Create a progress bar
            progress_bar = st.progress(0.0)
            for i in range(number_user):
                attribute_list = instance_generator.generate_instance()
                self.file_df.loc[len(self.file_df.index)] = attribute_list                
                # Update the progress bar with each iteration                            
                progress_bar.progress(text=f'Generating user {i + 1} from {number_user}', value=(i + 1) / number_user)                
        # Adding user_id column:
        user_id_list = list(range(1, number_user+1))
        self.file_df.insert(loc=0, column='user_id', value=user_id_list)
        return self.generate_null_values(self.file_df.copy())
