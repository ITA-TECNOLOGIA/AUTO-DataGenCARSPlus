from datagencars.synthetic_dataset.generator.generator_instance.generator_instance import GeneratorInstance
from datagencars.synthetic_dataset.generator.generator_output_file.generator_file import GeneratorFile

import random

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
            for _ in range(number_user):
                attribute_list = instance_generator.generate_instance()
                self.file_df.loc[len(self.file_df.index)] = attribute_list
        # Adding user_id column:
        user_id_list = list(range(1, number_user+1))
        self.file_df.insert(loc=0, column='user_id', value=user_id_list)
        return self.file_df.copy()

    def generate_null_values(self, complete_user_file):
        percentage_null = self.access_generation_config.get_number_user_null()
        if percentage_null > 0:
            number_user = self.access_generation_config.get_number_user()
            number_attributes = self.schema_access.get_number_attributes() - 1 #user_profile_id cannot be null
            null_values = int((number_attributes * number_user * percentage_null) / 100)
            # Generate random positions to be null
            for i in range(1, null_values+1):
                # Generate column to remove
                random_column = random.randint(1, number_attributes)
                # Generate row to remove
                random_row = random.randint(0, number_user-1)
                #print('Removing item column {} and row {}'.format(random_column, random_row))
                # Remove value
                if complete_user_file.iloc[random_row, random_column] != None:
                    complete_user_file.iloc[random_row, random_column] = None
                    i = i + 1
            #print(complete_user_file)
        return complete_user_file.copy()
         