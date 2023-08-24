from datagencars.synthetic_dataset.generate_synthetic_dataset import GenerateSyntheticDataset
from datagencars.synthetic_dataset.generator.generator_output_file.generator_rating_implicit import GeneratorImplicitRatingFile


class RatingImplicit(GenerateSyntheticDataset):
    """
    Class that generates a synthetic dataset with implicit ratings, using different schema files.

    Input files:    
        [GC]  generation_config.conf    
        [USc] user_schema.conf
        [UP]  user_profile.csv        
        [ISc] item_schema.conf
        [IP]  item_profile.conf                
        [CSc] context_schema.conf <optional>
        [BSc] behavior_schema.conf

    Output files:
        [U]  user.csv   
        [I]  item.csv
        [C]  context.csv <optional>
        [R]  rating.csv
    """    

    def __init__(self, generation_config):        
        super().__init__(generation_config)
         
    def generate_rating_file(self, item_df, behavior_df, with_context = False, context_df=None):
        """
            Generating file: rating.csv
        """
        rating_file_generator = GeneratorImplicitRatingFile(self.generation_config, item_df, behavior_df, context_df)
        return rating_file_generator.generate_file(with_context)
