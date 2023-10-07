import ast
import random

import numpy as np
import pandas as pd
from datagencars import util
from datagencars.existing_dataset.generate_user_profile.calculate_attribute_rating import CalculateAttributeRating
from datagencars.synthetic_dataset.generator.access_schema.access_generation_config import AccessGenerationConfig
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.access_schema.access_user_profile import AccessUserProfile


class GeneratorExplicitRatingFile:
    '''     
    Generates user ratings. For that purpose, it obtains random combinations
    <user, item, context> and computes the corresponding rating by applying the
    data utility function defined in the corresponding user profile. To compute
    the rating, this class takes into account whether the user profile defines a
    preference for higher or lower values in the domain of values of each
    attribute and transforms each attribute value into a normalized score in the
    output range required (e.g., a value between one and five), through linear
    regression. As real users do not rate items by applying a precise
    mathematical function, potential noise or uncertainty for the rating
    generated can be simulated by defining a weight different from zero for the
    attribute others in the user profile. More-over, this class generates a
    random time and date (within the input allowable range of dates provided)
    representing the time instant when the user provided the rating; random
    timestamps are generated in such a way that the ratings of the users are
    mixed with each other so supporting situations where several ratings are
    provided by the same or by different users at approximately the same time.
     
    @author Maria del Carmen Rodriguez-Hernandez 
    '''

    def __init__(self, generation_config, user_df, user_profile_df, item_df, item_schema, context_df=None, context_schema=None):        
        # User profile access: user_profile.csv        
        self.access_user_profile = AccessUserProfile(user_profile_df)
        # Schema access: generation_config.conf
        self.access_generation_config = AccessGenerationConfig(file_str=generation_config)
        # User file: user.csv
        self.user_df = user_df
        # Item file: item.csv
        self.item_df = item_df
        # Item schema: item_schema.conf
        self.item_schema_access = AccessSchema(file_str=item_schema)
        # Context:
        if context_df is None: 
            context_df = pd.DataFrame()
        if not context_df.empty and context_schema:
            # Context file (optional): context.csv
            self.context_df = context_df
            # Context schema: context_schema.conf
            self.context_schema_access = AccessSchema(file_str=context_schema)
        self.calculate_att_rating = CalculateAttributeRating()

    def generate_file(self, with_context=False):
        # sourcery skip: assign-if-exp, extract-duplicate-method, hoist-statement-from-loop, low-code-quality, merge-list-append, pandas-avoid-inplace
        '''
        Generates the rating file.
        :param with_context: True if the file to be generated will be contextual and False in the otherwise.
        :return: A dataframe with rating information (user_id, item_id, context_id <optional>, rating, timestamp). 
        '''     
        rating_df = None
        if with_context:
            rating_df = pd.DataFrame(columns=['user_id', 'item_id', 'context_id', 'rating', 'timestamp'])
        else:
            rating_df = pd.DataFrame(columns=['user_id', 'item_id', 'rating', 'timestamp'])

        # Getting the number of users.
        number_user = self.access_generation_config.get_number_user()
        user_id_list = self.user_df['user_id'].unique().tolist()
        # Getting the number of items.
        # number_item = self.access_generation_config.get_number_item()
        item_id_list = self.item_df['item_id'].unique().tolist()
        # Getting the number of contexts.
        if with_context:
            # number_context = self.access_generation_config.get_number_context()
            context_id_list = self.context_df['context_id'].unique().tolist()
        # Getting the number of ratings:
        number_ratings = self.access_generation_config.get_number_rating()
        print(f'Total of ratings to generate: {number_ratings}')
        print(f'Generating ratings by user.')        

        # Generating a timestamp list by day and in a range of years:
        minimum_date_ts = self.access_generation_config.get_minimum_date_timestamp()
        maximum_date_ts = self.access_generation_config.get_maximum_date_timestamp()
        start = pd.Timestamp(f'{minimum_date_ts}-01-01').strftime('%Y-%m-%d')
        end = pd.Timestamp(f'{maximum_date_ts}-12-31').strftime('%Y-%m-%d')
        timestamp_list = pd.date_range(start, end, freq='1d')

        # The k ratings to take in the past.
        k = self.access_generation_config.get_k_rating_past()
        # The minimum value rating.
        min_rating_value = self.access_generation_config.get_minimum_value_rating()
        # The maximum value rating.
        max_rating_value = self.access_generation_config.get_maximum_value_rating()
        # Even distribution.
        even_distribution = self.access_generation_config.get_even_distribution()
        
        # even_distribution=True: generating a similar count of ratings by user.
        if even_distribution:      
            # Determinig the number of rating by user:
            number_rating_by_user = int(number_ratings/number_user)
            ratings_by_user_list = [number_rating_by_user] * number_user
        else:
            # even_distribution=False: generating a random count of ratings by user.
            # Get the distribution type:
            distribution_type = self.access_generation_config.get_even_distribution_type()
            ratings_by_user_list, __, __ = self.get_number_of_ratings_by_user(number_user, number_ratings, distribution_type)                 

        # Iterating by user:
        for user_index in range(1, number_user+1):            
            row_rating_list = []
            # Generating user_id:
            user_id = user_id_list[user_index-1]
            print('user_id: ', user_id)
            row_rating_list.append(user_id)            
            # Determining the initial timestamp for the current user:
            initial_timestamp = timestamp_list[random.randint(0, len(timestamp_list)-1)]     
            # Check if the initial_timestamp is near to minimum year.
            while (initial_timestamp.year == minimum_date_ts) and (initial_timestamp.month == 12) and ((31-initial_timestamp.day) < number_rating_by_user):
                initial_timestamp = timestamp_list[random.randint(0, len(timestamp_list)-1)]
            
            # Generating ratings for the current user:
            user_rating_list = []                   
            number_rating_by_user = int(ratings_by_user_list[user_index-1])            
            for _ in range(number_rating_by_user):
                # Generating item_id:
                item_id = random.choice(item_id_list)
                row_rating_list.append(item_id)
                # Generating context_id:
                if with_context:
                    context_id = random.choice(context_id_list)
                    row_rating_list.append(context_id)
                # Generating a rating for a specified user profile:                   
                user_profile_id = self.user_df.loc[self.user_df['user_id'] == user_id, 'user_profile_id'].iloc[0]
                if with_context:
                    rating = self.get_rating(user_profile_id, item_id, context_id)
                else:
                    rating = self.get_rating(user_profile_id, item_id)        
                # Modifying the generated rating.                
                modified_rating = self.modify_rating_by_user_expectations(rating, k, user_rating_list, min_rating_value, max_rating_value)
                user_rating_list.append(rating)
                row_rating_list.append(modified_rating)
                # Generating timestamp:
                timestamp = initial_timestamp+pd.Timedelta(days=random.randint(1, 30), minutes=random.randint(1, 1440))                
                row_rating_list.append(timestamp)                
                # Inserting row into dataframe:                
                rating_df.loc[len(rating_df.index)] = row_rating_list  
                row_rating_list.clear()     
                row_rating_list.append(user_id)                

        if even_distribution:
            # Inserting remaining items to randomly selected users:
            number_remaining_rating = number_ratings - (number_rating_by_user*number_user)
            for _ in range(number_remaining_rating):
                row_rating_list.clear()
                # Choosing user_id:
                user_id = random.choice(user_id_list)
                row_rating_list.append(user_id)            
                # Generating item_id:
                item_id = random.choice(item_id_list)
                row_rating_list.append(item_id)
                # Generating context_id:
                if with_context:
                    context_id = random.choice(context_id_list)
                    row_rating_list.append(context_id)
                # Generating a rating for a specified user profile:            
                user_profile_id = self.user_df.loc[self.user_df['user_id'] == str(user_id), 'user_profile_id'].iloc[0]
                if with_context:
                    rating = self.get_rating(user_profile_id, item_id, context_id)
                else:
                    rating = self.get_rating(user_profile_id, item_id)
                # Modifying the generated rating.
                user_rating_list = rating_df.loc[rating_df['user_id'] == user_id]['rating'].tolist()
                modified_rating = self.modify_rating_by_user_expectations(rating, k, user_rating_list, min_rating_value, max_rating_value)
                row_rating_list.append(modified_rating)
                # Generating timestamp:
                timestamp_df = rating_df.loc[rating_df['user_id']==user_id, ['timestamp']]
                timestamp_df.sort_values(by='timestamp', ascending=False, inplace=True)
                initial_timestamp = timestamp_df['timestamp'].tolist()[0]
                timestamp = initial_timestamp+pd.Timedelta(days=random.randint(1, 30), minutes=random.randint(1, 1440))            
                row_rating_list.append(timestamp)
                # Inserting row into dataframe:
                rating_df.loc[len(rating_df.index)] = row_rating_list            

        # Sorting and returning a rating_df by user_id, item_id and/or context.
        rating_df = util.sort_rating_df(rating_df)      
        # Reseting index.
        rating_df.reset_index(drop=True, inplace=True)
        return rating_df
    
    def decrement_number_ratings_uniform(self, mi_lista, cantidad_a_decrementar):
        posiciones_no_cero = [i for i, valor in enumerate(mi_lista) if valor != 0]        
        if cantidad_a_decrementar > len(posiciones_no_cero):
            cantidad_a_decrementar = len(posiciones_no_cero)  
        indices_seleccionados = random.sample(posiciones_no_cero, cantidad_a_decrementar)        
        for indice in indices_seleccionados:  
            mi_lista[indice] -= 1
        return mi_lista

    def decrement_number_ratings_gaussian(self, mi_lista, cantidad_a_decrementar):
        posiciones_no_cero = [i for i, valor in enumerate(mi_lista) if valor != 0]          
        if cantidad_a_decrementar > len(posiciones_no_cero):
            cantidad_a_decrementar = len(posiciones_no_cero)
        centro = len(posiciones_no_cero) // 2  # Calcula el índice central de la lista
        inicio = max(0, centro - cantidad_a_decrementar // 2)  # Calcula el índice de inicio para seleccionar elementos
        fin = min(len(posiciones_no_cero), inicio + cantidad_a_decrementar)  # Calcula el índice de fin para seleccionar elementos
        indices_seleccionados = posiciones_no_cero[inicio:fin]  # Selecciona los elementos alrededor del centro          
        for indice in indices_seleccionados:  
            mi_lista[indice] -= 1  
        return mi_lista

    def increment_number_ratings_uniform(self, mi_lista, cantidad_a_incrementar):    
        if cantidad_a_incrementar > len(mi_lista):
            cantidad_a_incrementar = len(mi_lista)
        indices_seleccionados = random.sample(mi_lista, cantidad_a_incrementar)
        for indice in indices_seleccionados:  
            mi_lista[indice] += 1
        return mi_lista

    def increment_number_ratings_gaussian(self, mi_lista, cantidad_a_incrementar):  
        if cantidad_a_incrementar > len(mi_lista):
            cantidad_a_incrementar = len(mi_lista)  
        posiciones_lista = [i for i, __ in enumerate(mi_lista)]        
        centro = len(posiciones_lista) // 2  # Calcula el índice central de la lista
        inicio = max(0, centro - cantidad_a_incrementar // 2)  # Calcula el índice de inicio para seleccionar elementos
        fin = min(len(posiciones_lista), inicio + cantidad_a_incrementar)  # Calcula el índice de fin para seleccionar elementos
        indices_seleccionados = posiciones_lista[inicio:fin]  # Selecciona los elementos alrededor del centro        
        for indice in indices_seleccionados:  
            mi_lista[indice] += 1
        return mi_lista

    def get_number_of_ratings_by_user(self, number_user, number_ratings, distribution_type):
        # Define la media y la desviación estándar de la distribución gaussiana
        mu = 50 # media
        sigma = 10 # desviacion_estandar

        # Genera una lista de 90 números aleatorios que sigan una distribución gaussiana
        if distribution_type == 'uniform':
            random_proportions = np.random.uniform(mu, sigma, number_user)                
        elif distribution_type == 'gaussian':
            random_proportions = np.random.normal(mu, sigma, number_user)        

        # Normaliza la lista para que la suma sea igual a number_ratings
        suma_total = sum(random_proportions)
        numeros_normalizados = [int(round((x / suma_total) * number_ratings)) for x in random_proportions]        

        # Asegúrate de que la suma de los valores asignados sea igual a number_ratings
        diferencia = number_ratings - sum(numeros_normalizados)        
        if diferencia > 0:
            # Si la suma es menor que number_ratings, agrega la diferencia a uno de los valores
            if distribution_type == 'uniform':
                number_of_ratings_by_user = self.increment_number_ratings_uniform(numeros_normalizados, diferencia)
            elif distribution_type == 'gaussian':
                number_of_ratings_by_user = self.increment_number_ratings_gaussian(numeros_normalizados, diferencia)
        elif diferencia < 0:
            # Si la suma es mayor que number_ratings, resta la diferencia de uno de los valores    
            if distribution_type == 'uniform':
                number_of_ratings_by_user = self.decrement_number_ratings_uniform(numeros_normalizados, abs(diferencia))
            elif distribution_type == 'gaussian':
                number_of_ratings_by_user = self.decrement_number_ratings_gaussian(numeros_normalizados, abs(diferencia))    
        else:
            number_of_ratings_by_user = numeros_normalizados
        return number_of_ratings_by_user, numeros_normalizados, random_proportions

    def get_rating(self, user_profile_id, item_id, context_id=None):
        '''
        Determinig a rating value given weight and attribute rating vectors.
        :param user_profile_id: The user profile ID.
        :param item_id: The item ID.
        :param context_id: The context ID.
        :return: A rating value.
        '''       
        # Getting the attribute name list and atribute value list of the user_profile_id.        
        atribute_name_list, atribute_value_list = self.access_user_profile.get_vector_from_user_profile(user_profile_id)

        # Getting the current attribute value and its possible values.
        if context_id:
            attribute_value_list, attribute_possible_value_list = self.get_attribute_value_and_possible_value_list(atribute_name_list, item_id, context_id)
        else:
            attribute_value_list, attribute_possible_value_list = self.get_attribute_value_and_possible_value_list(atribute_name_list, item_id)                 
        # Getting the range of rating values:
        minimum_value_rating = self.access_generation_config.get_minimum_value_rating()
        maximum_value_rating = self.access_generation_config.get_maximum_value_rating() 
        # Getting the attribute rating vector.
        attribute_rating_vector = self.access_user_profile.get_attribute_rating_vector(atribute_value_list, attribute_value_list, attribute_possible_value_list, minimum_value_rating, maximum_value_rating, user_profile_attribute_list=atribute_name_list)

        if len(atribute_value_list) != len(attribute_rating_vector):
            raise ValueError('The vectors have not the same size.')
        
        rating = 0
        sum_weight = 0 # self.user_profile_df.loc[self.user_profile_df['user_profile_id'] == user_profile_id, 'other'].iloc[0]
        for idx, weight_importance in enumerate(atribute_value_list):
            # Getting importance and weight values:
            weight_importance_list = str(weight_importance).split('|')
            weight = 0
            if len(weight_importance_list) > 1:
                weight = float(weight_importance_list[1])
            else:
                weight = float(weight_importance)
            sum_weight += weight
            rating += weight * attribute_rating_vector[idx]
        if sum_weight != 1:            
            raise ValueError(f'The weights not sum 1 (sum weight: {sum_weight}). You must verify the user_profile.csv file (user profile: {user_profile_id}).')
        return round(rating, 2)
    
    def get_attribute_value_and_possible_value_list(self, atribute_name_list, item_id, context_id=None):
        '''
        Get the attribute value and its possible values.
        :param atribute_name_list: The list of attribute names.
        :param item_id: The item ID of the current user.
        :param context_id: The context ID of the current user <optional>.
        :return: The attribute value and its possible values.
        '''
        attribute_value_list = []
        possible_value_list = []
        for attribute_name in atribute_name_list:
            # Getting values from item.csv
            if attribute_name in list(self.item_df.columns.values):
                attribute_value = self.item_df.loc[self.item_df['item_id'] == item_id, attribute_name].iloc[0]                   
                # Check if the attribute value is None:
                if attribute_value is None:                    
                    attribute_value_list.append(None)                
                # Ckeck if is a list as str "['a', 'b']":
                elif (isinstance(attribute_value, str)) and ('[' in attribute_value):                                    
                    attribute_value_list.append(ast.literal_eval(attribute_value))                
                # For the cases of: list, bool, int and float values:
                else:                    
                    attribute_value_list.append(attribute_value)                
                # Getting possible values of the current attribute:         
                possible_value_list.append(self.item_schema_access.get_possible_values_attribute_list_from_name(attribute_name))
            elif context_id:
                # Getting values from context.csv
                print(list(self.context_df.columns.values))
                if attribute_name in list(self.context_df.columns.values):
                    attribute_value_list.append(self.context_df.loc[self.context_df['context_id'] == context_id, attribute_name].iloc[0])
                    # Getting possible values of the current attribute:
                    possible_value_list.append(self.context_schema_access.get_possible_values_attribute_list_from_name(attribute_name))
        return attribute_value_list, possible_value_list
    
    def modify_rating_by_user_expectations(self, rating, k, user_rating_list, min_rating_value, max_rating_value):
        '''
        Modifies the rating value with the user expectations.
        :param rating: The original rating (determined by using the user_profile).
        :param k: The k ratings to take in the past.
        :return: The modified rating value by using the user expectations.
        ''' 
        rating_modified = None        
        # Determinig the last k ratings of the current user in the past.
        number_ratings = len(user_rating_list)
        k_last_rating_list = []
        if (number_ratings < k) or (number_ratings == k):
            k_last_rating_list = user_rating_list
        else:            
            k_last_rating_list = user_rating_list[-k:]
        if len(k_last_rating_list) != 0:
            # Determing the rating average of the current user in the past:
            avg = np.average(k_last_rating_list)
            # Determining the percentage of variation, specified in the generation_config.conf file:
            percentage_rating_variation = self.access_generation_config.get_percentage_rating_variation()
            # Determining the rating variation:
            rating_variation = abs((rating - avg) * (percentage_rating_variation/100))              

            # Modifiying the rating value:
            if rating > avg:
                rating_modified = rating + rating_variation
            elif rating < avg:
                rating_modified = rating - rating_variation
            else:            
                rating_modified = rating # avg=0

            # Validating the modified rating value:
            if rating_modified > max_rating_value:
                # Avoid obtaining a modified rating higher than the maximum rating.
                rating_modified = min(max_rating_value, rating_modified)
            elif rating_modified < min_rating_value:
                # Avoid obtaining a modified rating lower than the minimum rating.
                rating_modified = max(min_rating_value, rating_modified)
        else:
            rating_modified = rating
        return int(round(rating_modified))
