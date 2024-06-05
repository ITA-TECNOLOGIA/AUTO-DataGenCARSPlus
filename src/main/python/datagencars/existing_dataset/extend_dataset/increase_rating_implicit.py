import pandas as pd
import random
from datetime import datetime
from datagencars.synthetic_dataset.generator.generator_output_file.generator_implicit_rating_file import GeneratorImplicitRatingFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_behavior_file import GeneratorBehaviorFile


class IncreaseRatingImplicit():
    
    def __init__(self, generation_config_behavior, generation_config_rating, behavior_schema, behavior_df, item_df, item_schema, context_df):
        self.with_context = False
        if not context_df.empty:
            self.with_context = True
            self.context_df = context_df
        # Crear instancias de los generadores
        self.behavior_generator = GeneratorBehaviorFile(generation_config_behavior, behavior_schema, item_df, item_schema)
        self.rating_generator = GeneratorImplicitRatingFile(generation_config_rating, item_df, behavior_df, context_df)

    def extend_rating_by_user(self, number_rating):
        pass

    def extend_rating_random(self, number_rating, percentage_rating_variation=None, k=None):
        generated_ratings_count = 0
        extended_ratings = pd.DataFrame()
        extended_behavior = pd.DataFrame()

        while generated_ratings_count < number_rating:
            # Generar un nuevo comportamiento
            user_id = random.randint(1, self.behavior_generator.num_users)
            context_id = random.randint(1, self.behavior_generator.num_contexts)
            current_time = random.uniform(self.behavior_generator.minimum_year_ts, self.behavior_generator.maximum_year_ts)
            self.behavior_generator.generate_session_times(user_id, context_id, self.behavior_generator.item_df, current_time)

            filtered_behavior_df = self.rating_generator.preprocess_behavior_df(with_context=True)
            # Evaluar cada comportamiento generado para obtener una valoración implícita
            for index, behavior_row in filtered_behavior_df.iterrows():
                new_rating, timestamp = self.rating_generator.get_rating_and_timestamp(behavior_row, self.behavior_generator.file_df)
                if new_rating is not None:
                    generated_ratings_count += 1

                    # Convert the Unix timestamp to a datetime object
                    timestamp_datetime = datetime.fromtimestamp(timestamp)

                    # Format the datetime object as a string
                    timestamp_str = timestamp_datetime.strftime('%Y-%m-%d %H:%M:%S')

                    # Create a new instance with all necessary elements
                    new_instance = {
                        'user_id': behavior_row['user_id'],
                        'item_id': behavior_row['item_id'],
                        'rating': new_rating,
                        'timestamp': timestamp_str
                    }
                    if self.with_context:
                        new_instance['context_id'] = behavior_row['context_id']

                    # Convert the instance into a DataFrame and append it to extended_ratings
                    new_instance_df = pd.DataFrame([new_instance])
                    extended_ratings = pd.concat([extended_ratings, new_instance_df], ignore_index=True)

                    extended_behavior = extended_behavior.append(behavior_row)
                    
                    if generated_ratings_count >= number_rating:
                        break

            # Reiniciar el DataFrame de comportamientos para la siguiente iteración
            self.behavior_generator.file_df = pd.DataFrame()

        return extended_behavior, extended_ratings

""" Ejemplo de uso de la clase IncreaseRatingImplicit:
schema_path = 'resources/data_schema_imascono/'
with open(schema_path + 'generation_config.conf', 'r') as generation_config_file:
    generation_config = generation_config_file.read()  
with open(schema_path + 'behavior_schema.conf', 'r') as behavior_schema_file:
    behavior_schema = behavior_schema_file.read()
with open(schema_path + 'item_schema.conf', 'r') as item_schema_file:
    item_schema = item_schema_file.read()

df_path = 'resources/dataset_imascono/Paper/'
item_df = pd.read_csv(df_path + 'item.csv', encoding='utf-8', index_col=False)
behavior_df = pd.read_csv(df_path + 'behavior2.csv', encoding='utf-8', index_col=False)
context_df = pd.read_csv(df_path + 'context.csv', encoding='utf-8', index_col=False)

# Ejemplo de llamada a la función para generar 100 nuevas valoraciones
increase = IncreaseRatingImplicit(generation_config, behavior_schema, behavior_df, item_df, item_schema, context_df)
new_behaviors, new_ratings = increase.extend_rating_random(100)

# Append new_behaviors to the existing behaviors dataset
existing_behaviors_df = pd.read_csv(r'resources\dataset_imascono\Paper\behavior2.csv')
updated_behaviors_df = pd.concat([existing_behaviors_df, new_behaviors]).reset_index(drop=True)
# Cast 'context_id' to int
updated_behaviors_df['context_id'] = updated_behaviors_df['context_id'].fillna(0).astype(int)

updated_behaviors_df = updated_behaviors_df.sort_values(by=['user_id']).reset_index(drop=True)
updated_behaviors_df.to_csv(r'resources\dataset_imascono\Paper\extended_behavior2.csv', index=False)

# Append new_ratings to the existing ratings dataset
existing_ratings_df = pd.read_csv(r'resources\dataset_imascono\Paper\rating.csv')
updated_ratings_df = pd.concat([existing_ratings_df, new_ratings]).reset_index(drop=True)
# Cast 'context_id' to int
updated_ratings_df['context_id'] = updated_ratings_df['context_id'].fillna(0).astype(int)

updated_ratings_df = updated_ratings_df.sort_values(by=['user_id']).reset_index(drop=True)
updated_ratings_df.to_csv(r'resources\dataset_imascono\Paper\extended_ratings.csv', index=False)
"""