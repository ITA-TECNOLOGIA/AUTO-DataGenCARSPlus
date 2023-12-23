import pandas as pd
import random

from datagencars.synthetic_dataset.generator.generator_output_file.generator_implicit_rating_file import GeneratorImplicitRatingFile
from datagencars.synthetic_dataset.generator.generator_output_file.generator_behavior_file import GeneratorBehaviorFile

# def extend_ratings_dataset(number_of_ratings_to_generate, behavior_generator, rating_generator):
#     generated_ratings_count = 0
#     extended_ratings = pd.DataFrame()

#     while generated_ratings_count < number_of_ratings_to_generate:
#         # Generar un nuevo comportamiento
#         new_behavior = behavior_generator.generate_behavior()

#         # Evaluar el nuevo comportamiento para generar una valoración implícita
#         new_rating = rating_generator.evaluate_behavior(new_behavior)

#         # Si se genera una nueva valoración, incrementar el contador y anexarla al conjunto de datos
#         if new_rating is not None:
#             generated_ratings_count += 1
#             extended_ratings = extended_ratings.append(new_rating, ignore_index=True)
            
#     return extended_ratings

def extend_ratings_dataset(number_of_ratings_to_generate, behavior_generator, rating_generator):
    generated_ratings_count = 0
    extended_ratings = pd.DataFrame()

    while generated_ratings_count < number_of_ratings_to_generate:
        # Generar un nuevo comportamiento
        user_id = random.randint(1, behavior_generator.num_users)
        context_id = random.randint(1, behavior_generator.num_contexts)
        current_time = random.uniform(behavior_generator.minimum_year_ts, behavior_generator.maximum_year_ts)
        behavior_generator.generate_session_times(user_id, context_id, behavior_generator.item_df, current_time)

        filtered_behavior_df = rating_generator.preprocess_behavior_df(with_context=True)
        # Evaluar cada comportamiento generado para obtener una valoración implícita
        for index, behavior_row in filtered_behavior_df.iterrows():
            new_rating = rating_generator.get_rating_and_timestamp(behavior_row, behavior_generator.file_df)
            if new_rating is not None:
                generated_ratings_count += 1
                # extended_ratings = extended_ratings.append(int(new_rating[0]), ignore_index=True)
                new_rating_series = pd.Series(new_rating[0])
                extended_ratings = extended_ratings.append(new_rating_series, ignore_index=True)
                if generated_ratings_count >= number_of_ratings_to_generate:
                    break

        # Reiniciar el DataFrame de comportamientos para la siguiente iteración
        behavior_generator.file_df = pd.DataFrame()

    return extended_ratings

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

# Crear instancias de los generadores
behavior_generator = GeneratorBehaviorFile(generation_config, behavior_schema, item_df, item_schema)
rating_generator = GeneratorImplicitRatingFile(generation_config, item_df, behavior_df, context_df)

# Ejemplo de llamada a la función para generar 100 nuevas valoraciones
new_ratings = extend_ratings_dataset(100, behavior_generator, rating_generator)

# Aquí se debería anexar 'new_ratings' al conjunto de datos de valoraciones existente
existing_ratings_df = pd.read_csv(r'resources\dataset_imascono\Paper\rating.csv')
updated_ratings_df = pd.concat([existing_ratings_df, new_ratings]).reset_index(drop=True)
updated_ratings_df.to_csv(r'resources\dataset_imascono\Paper\updated_ratings.csv', index=False)
