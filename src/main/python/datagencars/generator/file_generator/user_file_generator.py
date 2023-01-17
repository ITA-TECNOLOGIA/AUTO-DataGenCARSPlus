import logging

from datagencars.generator.file_generator.file_generator import FileGenerator
from datagencars.generator.instance_generator.instance_gaussian_generator import InstanceGaussianGenerator
from datagencars.generator.instance_generator.instance_random_generator import InstanceRandomGenerator


class UserFileGenerator(FileGenerator):
    '''
    Generator of the user file (user.csv), by using configuration files. 
    The resulting file contains information related to users (e.g., user_id, age, gender, occupation, birthdate, etc.).  
    The following files are required: generation_config.conf and user_schema.conf.  
    '''

    def __init__(self, generation_file_path, user_schema_file_path):
        super().__init__(generation_file_path, user_schema_file_path)

    def generate_file(self):
        '''
        Generates the user file.        
        :return: A dataframe with user information.         
        '''
        instance_generator = None
        if self.generation_access.is_gaussian_distribution():
            # Gaussian distribution:
            instance_generator = InstanceGaussianGenerator(generation_access=self.generation_access, schema_access=self.schema_access)        
        else:
            # Random without correlation:
            instance_generator = InstanceRandomGenerator(generation_access=self.generation_access, schema_access=self.schema_access)

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