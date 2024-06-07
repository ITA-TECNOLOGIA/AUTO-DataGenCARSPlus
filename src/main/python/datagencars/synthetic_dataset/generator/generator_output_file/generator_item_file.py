import streamlit as st
from datagencars.synthetic_dataset.generator.access_schema.access_item_profile import AccessItemProfile
from datagencars.synthetic_dataset.generator.generator_instance.generator_instance import GeneratorInstance
from datagencars.synthetic_dataset.generator.generator_output_file.generator_file import GeneratorFile


class GeneratorItemFile(GeneratorFile):
    '''
    Generator of the item file (item.csv), by using configuration files. 
    The resulting file contains information related to items (e.g., item_id, web_name, address, province, country, phone, weekday_is_open, etc.).  
    The following files are required: generation_config.conf, item_schema.conf and item_profile.conf.  
    '''

    def __init__(self, generation_config, item_schema, item_profile=None):
        super().__init__(generation_config, item_schema)
        # Acces item profile.
        if item_profile:
            self.item_profile_access = AccessItemProfile(file_str=item_profile)
        else:
            self.item_profile_access = None    

    def generate_file(self, input_csv=None):
        '''
        Generates the item file.        
        :return: A dataframe with item information.
        '''
        # Create a progress bar
        progress_bar = st.progress(0.0)
        instance_generator = None
        if self.access_generation_config != None:
            # Number of items to be generated.
            number_item = self.access_generation_config.get_number_item()
        else:
            number_item = len(input_csv)      
        print(f'Total of items to generate: {number_item}')
        print('Generating instances by item.')
        # Check if apply correlation between attibutes:
        if self.item_profile_access:
            # Random with correlation:
            instance_generator = GeneratorInstance(generation_access=self.access_generation_config, schema_access=self.schema_access, item_profile_access=self.item_profile_access)
            number_profile = self.item_profile_access.get_number_profiles()
            current_number_item_by_profile = 0
            for position_item_profile in range(1, number_profile+1):                
                # Determining the number of instances to generate by item profile:
                probability_percentage_profile = self.access_generation_config.get_probability_percentage_profile_from_pos(position=position_item_profile)
                number_item_by_profile = (probability_percentage_profile*number_item)/100
                # Determining the number of noise in the instances to generate by item profile:
                noise_percentage_profile = self.access_generation_config.get_noise_percentage_profile_from_pos(position=position_item_profile)
                number_noise_by_profile = int((noise_percentage_profile*number_item_by_profile)/100)                
                for i in range(number_noise_by_profile):
                    attribute_list = instance_generator.generate_instance(position_item_profile=position_item_profile, with_noise=True)
                    self.file_df.loc[len(self.file_df.index)] = attribute_list                    
                    # Update the progress bar with each iteration                    
                    current_number_item_by_profile += 1
                    progress_bar.progress(text=f'Generating {current_number_item_by_profile} items from {number_item}', value=(current_number_item_by_profile) / number_item)
                for i in range(int(number_item_by_profile)-number_noise_by_profile):
                    attribute_list = instance_generator.generate_instance(position_item_profile=position_item_profile, with_noise=False)
                    self.file_df.loc[len(self.file_df.index)] = attribute_list
                    # Update the progress bar with each iteration
                    current_number_item_by_profile += 1
                    progress_bar.progress(text=f'Generating {current_number_item_by_profile} items from {number_item}', value=(current_number_item_by_profile) / number_item)                    
            # Check if there are pending items to be added in self.file_df: without correlation
            count_pending_items = number_item - len(self.file_df)
            if count_pending_items > 0:     
                instance_generator = GeneratorInstance(schema_access=self.schema_access)
                for count_pend_item in range(1, count_pending_items+1):                    
                    attribute_list = instance_generator.generate_instance()
                    self.file_df.loc[len(self.file_df.index)] = attribute_list
                    # Update the progress bar with each iteration
                    progress_bar.progress(text=f'Generating {current_number_item_by_profile+count_pend_item} items from {number_item}', value=(current_number_item_by_profile+count_pend_item) / number_item)
        else:
            # Without correlation (Random or Gaussian distribution):
            instance_generator = GeneratorInstance(schema_access=self.schema_access)
            for i in range(number_item):
                if not(input_csv is None):
                    instance = input_csv.iloc[i]
                else:
                    instance = None
                attribute_list = instance_generator.generate_instance(instance=instance)           
                self.file_df.loc[len(self.file_df.index)] = attribute_list
                # Update the progress bar with each iteration
                progress_bar.progress(text=f'Generating {i + 1} items from {number_item}', value=(i + 1) / number_item) 
        # Adding item_id column:
        item_id_list = list(range(1, number_item+1))
        self.file_df.insert(loc=0, column='item_id', value=item_id_list)
        if 'object_type' in self.file_df.columns:
            self.file_df = self.update_object_action(self.file_df)        
        if 'object_position' in self.file_df.columns:
            #Extract the 4th element from the object_position list and insert it into a new room_id column
            self.file_df['room_id'] = self.file_df['object_position'].apply(lambda x: x.pop(3))
        # Generating nulls values:             
        percentage_null_value_global = self.access_generation_config.get_percentage_null_value_global()
        percentage_null_value_attribute_list = self.access_generation_config.get_percentage_null_value_attribute()        
        if (percentage_null_value_global is not None) and (percentage_null_value_global > 0):        
            return self.generate_null_value_global(self.file_df.copy(), percentage_null_value_global)
        elif len(percentage_null_value_attribute_list) != 0:
            return self.generate_null_value_attribute(self.file_df.copy(), percentage_null_value_attribute_list)
        else:
            return self.file_df.copy()
    
    def update_object_action(self, df):
        """
        Update the 'object_action_types' column in the dataframe based on the 'object_type' column.
        :param df: The dataframe containing the data to be updated.
        :return: The dataframe with the 'object_action_types' column updated.
        """
        for index, row in df.iterrows():
            object_type = row['object_type']
            object_action = row['object_action_types']
            df.at[index, 'object_action_types'] = object_action[object_type]
        return df
