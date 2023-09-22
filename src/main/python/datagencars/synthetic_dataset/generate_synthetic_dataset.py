from abc import ABC, abstractmethod

from datagencars.synthetic_dataset.generator.generator_output_file.generator_behavior import GeneratorBehaviorFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_context import GeneratorContextFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_item import GeneratorItemFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_user import GeneratorUserFile


class GenerateSyntheticDataset(ABC):
    """
        Abstract parent class that generates a synthetic dataset, using different schema files as input.   

        The algorithm consists of five layers, each of them representing a module and its role in creating the synthetic dataset:
        - Layer 1: The Access Data Layer (access_data.py) parses the configuration schemes. It is responsible for reading and interpreting the configuration instructions set by the user, preparing the system for the data generation phase.
        - Layer 2: The Attribute Generation Layer (generator_attribute.py) generates individual attributes, by using the Access Data Layer. Depending on the configuration schemes, the attributes could be of several
        - Layer 3: The Instance Generation Layer (generator_instance.py) generates instances of each attribute type. It uses the attributes generated by the previous layer and generates individual instances that will form part of the synthetic dataset.
        - Layer 4: The File Generation Layer (generator_file.py): generates each file (user, item, context<optional>, behavior and rating) based on the attributes and instances from the previous layers. The files created are comprehensive and aligned with the original configuration schemes.
        - Layer 5: The Synthetic Dataset Generation Layer (generate_synthetic_dataset.py) calls all the previous layer together, generating the synthetic dataset. It ensures all the layers work in harmony and the final dataset is as per the configuration schemes provided by the user.
    """    

    def __init__(self, generation_config):
        self.generation_config = generation_config

    def generate_user_file(self, user_schema):
        """
            Generating file: user.csv
        """        
        user_file_generator = GeneratorUserFile(self.generation_config, user_schema)
        complete_user_file = user_file_generator.generate_file()
        return user_file_generator.generate_null_values(complete_user_file)
    
    def generate_item_file(self, item_schema, item_profile=None, with_correlation=False):
        """
            Generating file: item.csv
        """        
        item_file_generator = GeneratorItemFile(item_schema, self.generation_config, item_profile)
        complete_item_file = item_file_generator.generate_file(with_correlation)  
        return item_file_generator.generate_null_values(complete_item_file)

    def generate_context_file(self, context_schema):
        """
            Generating file (for CARS): context.csv
        """        
        context_file_generator = GeneratorContextFile(context_schema, self.generation_config)
        complete_context_file = context_file_generator.generate_file()
        return context_file_generator.generate_null_values(complete_context_file)
    
    def generate_behavior_file(self, behavior_schema, item_df, item_schema):
        """
            Generating file (for CARS): behavior.csv
        """        
        behavior_file_generator = GeneratorBehaviorFile(self.generation_config, behavior_schema, item_df, item_schema)
        return behavior_file_generator.generate_file()
    
    @abstractmethod
    def generate_rating_file(self, user_df, user_profile_df, item_df, item_schema, with_context=False, context_df=None, context_schema=None):
        """
            Generating file: rating.csv
        """
        pass