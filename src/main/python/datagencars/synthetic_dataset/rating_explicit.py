from datagencars.synthetic_dataset.generator.generator_output_file.generator_rating_explicit import GeneratorExplicitRatingFile
from datagencars.synthetic_dataset.generate_synthetic_dataset import GenerateSyntheticDataset


class RatingExplicit(GenerateSyntheticDataset):
    """
    Class that generates a synthetic dataset with explicit ratings, using different schema files.

    Input files:    
        [GC]  generation_config.conf    
        [USc] user_schema.conf
        [UP]  user_profile.csv        
        [ISc] item_schema.conf
        [IP]  item_profile.conf                
        [CSc] context_schema.conf <optional>

    Output files:
        [U]  user.csv   
        [I]  item.csv
        [C]  context.csv <optional>
        [R]  rating.csv
    """    

    def __init__(self, generation_config):
        super().__init__(generation_config)

    def generate_rating_file(self, user_df, user_profile_df, item_df, item_schema, with_context=False, context_df=None, context_schema=None):
        """
            Generating file: rating.csv
        """
        rating_file_generator = GeneratorExplicitRatingFile(self.generation_config, user_df, user_profile_df, item_df, item_schema, context_df, context_schema)
        return rating_file_generator.generate_file(with_context)
