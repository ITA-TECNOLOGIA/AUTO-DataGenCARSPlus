from datagencars.synthetic_dataset.generate_synthetic_dataset import GenerateSyntheticDataset
from datagencars.synthetic_dataset.generator.generator_output_file.generator_implicit_rating_file import GeneratorImplicitRatingFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_behavior_file import GeneratorBehaviorFile


class GenerateSyntheticImplicitDataset(GenerateSyntheticDataset):
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
         
    def generate_rating_file(self, item_df, behavior_df, with_context=False, context_df=None):
        """
            Generating file: rating.csv
        """
        rating_file_generator = GeneratorImplicitRatingFile(self.generation_config, item_df, behavior_df, context_df)
        return rating_file_generator.generate_file(with_context)
    
    def generate_behavior_file(self, behavior_schema, item_df, item_schema):
        """
            Generating file (for CARS): behavior.csv
        """        
        behavior_file_generator = GeneratorBehaviorFile(generation_config=self.generation_config, behavior_schema=behavior_schema, item_df=item_df, item_schema=item_schema)
        return behavior_file_generator.generate_file()
