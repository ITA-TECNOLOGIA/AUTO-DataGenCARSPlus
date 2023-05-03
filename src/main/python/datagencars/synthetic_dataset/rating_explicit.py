import logging

from datagencars.synthetic_dataset.generator.generator_output_file.generator_rating_explicit import GeneratorExplicitRatingFile
from datagencars.synthetic_dataset.generate_synthetic_dataset import GenerateSyntheticDataset


class RatingExplicit(GenerateSyntheticDataset):
    '''
    Generates a synthetic dataset.

    Input:    
        [GC] generation_config.conf    
        [US] user_schema.conf
        [UP] user_profile.csv
        [U]  user.csv    
        [IS] item_schema.conf
        [IP] item_profile.conf
        [I]  item.csv
        [CS] context_schema.conf <optional>
        [C]  context.csv <optional>
        [R]  rating.csv

    Algorithm:
        1- acces_schema: Access to schema information.
        2- generator_attribute: Generate attributes, by using acces_schema.
        3- generator_instance: Generate instances, by using generator_attribute.
        4- generator_output_file: Generate user, item, context <optional>, rating files, by using generator_instance.
        5- generate_synthetic_dataset: Generate all output files, by using generator_output_file.

    Output:
        [U]  user.csv   
        [I]  item.csv
        [C]  context.csv <optional>
        [R]  rating.csv
    '''    

    def __init__(self, generation_config):
        super().__init__(generation_config)

    def generate_rating_file(self, user_df, user_profile_df, item_df, item_schema, with_context=False, context_df=None, context_schema=None):
        '''
            Generating file: rating.csv
        '''
        rating_file_generator = GeneratorExplicitRatingFile(self.generation_config, user_df, user_profile_df, item_df, item_schema, context_df, context_schema)
        return rating_file_generator.generate_file(with_context)
