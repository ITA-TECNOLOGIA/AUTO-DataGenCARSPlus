import logging

from datagencars.synthetic_dataset.generator.generator_instance.generator_instance_gaussian import GeneratorInstanceGaussian
from datagencars.synthetic_dataset.generator.generator_instance.generator_instance_random import GeneratorInstanceRandom
from datagencars.synthetic_dataset.generator.generator_output_file.generator_file import GeneratorFile


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
        instance_generator = None
        if self.generation_access.is_gaussian_distribution():
            # Gaussian distribution:
            instance_generator = GeneratorInstanceGaussian(generation_access=self.generation_access, schema_access=self.schema_access)        
        else:
            # Random without correlation:
            instance_generator = GeneratorInstanceRandom(generation_access=self.generation_access, schema_access=self.schema_access)

        # Number of users to be generated.
        number_user = self.generation_access.get_number_user()
        for _ in range(number_user):           
            attribute_list = instance_generator.generate_instance()
            self.file_df.loc[len(self.file_df.index)] = attribute_list

        # Adding user_id column:
        user_id_list = list(range(1, number_user+1))
        self.file_df.insert(loc=0, column='user_id', value=user_id_list)
        return self.file_df.copy()


# generation_file_path = 'resources/data/generation_config.conf'
# user_schema_file_path = 'resources/data/user_schema.conf'
# user_file_generator = UserFileGenerator(generation_file_path, user_schema_file_path)
# user_file_df = user_file_generator.generate_file()
# print(user_file_df)