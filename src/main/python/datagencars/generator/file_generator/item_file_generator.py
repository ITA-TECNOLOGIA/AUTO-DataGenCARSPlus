import logging

from datagencars.generator.file_generator.file_generator import FileGenerator
from datagencars.generator.instance_generator.instance_gaussian_generator import InstanceGaussianGenerator
from datagencars.generator.instance_generator.instance_random_generator import InstanceRandomGenerator
from datagencars.generator.instance_generator.instance_correlation_generator import InstanceCorrelationGeneration


class ItemFileGenerator(FileGenerator):
    '''
    Generator of the item file (item.csv), by using configuration files. 
    The resulting file contains information related to items (e.g., item_id, web_name, address, province, country, phone, weekday_is_open, etc.).  
    The following files are required: generation_config.conf, item_schema.conf and item_profile.conf.  
    '''

    def __init__(self, generation_file_path, item_schema_file_path, item_profile_file_path):
        super().__init__(generation_file_path, item_schema_file_path, item_profile_file_path)           

    def generate_file(self, with_correlation):
        '''
        Generates the item file.
        :param with_correlation: True if the generation of attribute values by instance is correlated with an item profile, and False otherwise.
        :return: A dataframe with item information.         
        '''
        instance_generator = None
        if self.generation_access.is_gaussian_distribution():
            # Gaussian distribution:
            instance_generator = InstanceGaussianGenerator(generation_access=self.generation_access, schema_access=self.schema_access)
        elif with_correlation:
            # Random with correlation:
            instance_generator = InstanceCorrelationGeneration(generation_access=self.generation_access, schema_access=self.schema_access, item_profile_access=self.item_profile_access)
        else:
            # Random without correlation:
            instance_generator = InstanceRandomGenerator(generation_access=self.generation_access, schema_access=self.schema_access)

        # Number of items to be generated.
        number_item = self.generation_access.get_number_item()
        if with_correlation:
            # With correlation (Random):
            number_profile = self.item_profile_access.get_number_profiles()
            for position_item_profile in range(1, number_profile+1):
                # Determining the number of instances to generate by item profile:
                probability_percentage_profile = self.generation_access.get_probability_percentage_profile_from_pos(position=position_item_profile)
                number_item_by_profile = (probability_percentage_profile*number_item)/100
                # Determining the number of noise in the instances to generate by item profile:
                noise_percentage_profile = self.generation_access.get_noise_percentage_profile_from_pos(position=position_item_profile)
                number_noise_by_profile = int((noise_percentage_profile*number_item_by_profile)/100)
                for _ in range(number_noise_by_profile):
                    attribute_list = instance_generator.generate_instance(position_item_profile=position_item_profile, with_noise=True)
                    self.file_df.loc[len(self.file_df.index)] = attribute_list
                for _ in range(int(number_item_by_profile)-number_noise_by_profile):                                       
                    attribute_list = instance_generator.generate_instance(position_item_profile=position_item_profile, with_noise=False)
                    self.file_df.loc[len(self.file_df.index)] = attribute_list                         
        else:
            # Without correlation (Random or Gaussian distribution):
            for _ in range(number_item):            
                attribute_list = instance_generator.generate_instance()
            self.file_df.loc[len(self.file_df.index)] = attribute_list

        # Adding item_id column:
        item_id_list = list(range(1, number_item+1))
        self.file_df.insert(loc=0, column='item_id', value=item_id_list)
        return self.file_df.copy()


# generation_file_path = 'resources/data/generation_config.conf'
# item_schema_file_path = 'resources/data/item_schema.conf'
# item_profile_file_path = 'resources/data/item_profile.conf'
# item_file_generator = ItemFileGenerator(generation_file_path, item_schema_file_path, item_profile_file_path)
# item_file_df = item_file_generator.generate_file(with_correlation=True)
# print(item_file_df)