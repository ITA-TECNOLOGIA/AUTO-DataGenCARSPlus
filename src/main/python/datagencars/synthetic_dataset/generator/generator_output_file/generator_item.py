import logging

from datagencars.synthetic_dataset.generator.generator_instance.generator_instance import GeneratorInstance
from datagencars.synthetic_dataset.generator.generator_output_file.generator_file import GeneratorFile


class GeneratorItemFile(GeneratorFile):
    '''
    Generator of the item file (item.csv), by using configuration files. 
    The resulting file contains information related to items (e.g., item_id, web_name, address, province, country, phone, weekday_is_open, etc.).  
    The following files are required: generation_config.conf, item_schema.conf and item_profile.conf.  
    '''

    def __init__(self, generation_config, item_schema, item_profile):
        super().__init__(generation_config, item_schema, item_profile)           

    def generate_file(self, with_correlation):
        '''
        Generates the item file.        
        :return: A dataframe with item information.         
        '''
        instance_generator = None
        # Number of items to be generated.
        number_item = self.access_generation_config.get_number_item()
        print(f'Total of items to generate: {number_item}')
        print('Generating instances by item.')        
        if with_correlation:
            # Random with correlation:
            instance_generator = GeneratorInstance(generation_access=self.access_generation_config, schema_access=self.schema_access, item_profile_access=self.item_profile_access)
            number_profile = self.item_profile_access.get_number_profiles()
            for position_item_profile in range(1, number_profile+1):
                # Determining the number of instances to generate by item profile:
                probability_percentage_profile = self.access_generation_config.get_probability_percentage_profile_from_pos(position=position_item_profile)
                number_item_by_profile = (probability_percentage_profile*number_item)/100
                # Determining the number of noise in the instances to generate by item profile:
                noise_percentage_profile = self.access_generation_config.get_noise_percentage_profile_from_pos(position=position_item_profile)
                number_noise_by_profile = int((noise_percentage_profile*number_item_by_profile)/100)
                for _ in range(number_noise_by_profile):
                    attribute_list = instance_generator.generate_instance(position_item_profile=position_item_profile, with_noise=True)
                    self.file_df.loc[len(self.file_df.index)] = attribute_list
                for _ in range(int(number_item_by_profile)-number_noise_by_profile):                                       
                    attribute_list = instance_generator.generate_instance(position_item_profile=position_item_profile, with_noise=False)
                    self.file_df.loc[len(self.file_df.index)] = attribute_list                         
        else:
            # Without correlation (Random or Gaussian distribution):
            instance_generator = GeneratorInstance(schema_access=self.schema_access)
            for _ in range(number_item):            
                attribute_list = instance_generator.generate_instance()
                self.file_df.loc[len(self.file_df.index)] = attribute_list            

        # Adding item_id column:
        item_id_list = list(range(1, number_item+1))        
        self.file_df.insert(loc=0, column='item_id', value=item_id_list)
        return self.file_df.copy()
