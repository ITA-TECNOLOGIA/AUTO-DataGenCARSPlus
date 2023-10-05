import logging
from configparser import NoOptionError, NoSectionError
import ast
from datagencars.synthetic_dataset.generator.access_schema.access_data import AccessData


class AccessGenerationConfig(AccessData):
    '''
    Access to the values of the properties stored in the file generation_config.txt.
    @author Maria del Carmen Rodriguez-Hernandez 
    '''
    
    def __init__(self, file_str):
        super().__init__(file_str)
    
    def get_number_user(self):
        '''
        Gets the number of users to generate in the dataset.
        :return: The number of users to generate in the dataset.
        '''
        number_user = None
        try:
            number_user = self.file_parser.getint(section='dimension', option='number_user')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return number_user

    def get_number_item(self):
        '''
        Gets the number of items to generate in the dataset.
        :return: The number of items to generate in the dataset.
        '''
        number_item = None
        try:
            number_item = self.file_parser.getint(section='dimension', option='number_item')
        except (NoOptionError, NoSectionError) as e:            
            logging.error(e)
        return number_item

    def get_number_context(self):
        '''
        Gets the number of contexts to generate in the dataset.
        :return: The number of items to generate in the dataset.
        '''
        number_context = None
        try:
            number_context = self.file_parser.getint(section='dimension', option='number_context')
        except (NoOptionError, NoSectionError) as e:            
            logging.error(e)
        return number_context 
    
    def get_number_user_null(self):
        '''
        Gets the percentage of null user values to generate in the dataset.
        :return: The percentage of null values to generate in the dataset.
        '''
        percentage_user_null = None
        try:
            percentage_user_null = self.file_parser.getint(section='dimension', option='percentage_user_null_value')
        except (NoOptionError, NoSectionError) as e:            
            logging.error(e)
        return percentage_user_null 
    
    def get_number_item_null(self):
        '''
        Gets the percentage of null item values to generate in the dataset.
        :return: The percentage of null values to generate in the dataset.
        '''
        percentage_item_null = None
        try:
            percentage_item_null = self.file_parser.getint(section='dimension', option='percentage_item_null_value')
        except (NoOptionError, NoSectionError) as e:            
            logging.error(e)
        return percentage_item_null 
    
    def get_number_context_null(self):
        '''
        Gets the percentage of null context values to generate in the dataset.
        :return: The percentage of null values to generate in the dataset.
        '''
        percentage_context_null = None
        try:
            percentage_context_null = self.file_parser.getint(section='dimension', option='percentage_context_null_value')
        except (NoOptionError, NoSectionError) as e:            
            logging.error(e)
        return percentage_context_null 

    def get_number_rating(self):
        '''
        Gets the number of ratings to generate in the dataset.
        :return: The number of ratings to generate in the dataset.
        '''
        number_rating = None
        try:
            number_rating = self.file_parser.getint(section='rating', option='number_rating')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return number_rating

    def get_minimum_value_rating(self):
        '''
        Gets the minimum value of the rating.
        :return: The minimum value of the rating.
        '''
        minimum_value_rating = None
        try:
            minimum_value_rating = self.file_parser.getfloat(section='rating', option='minimum_value_rating')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return minimum_value_rating

    def get_maximum_value_rating(self):
        '''
        Gets the maximum value of the rating.
        :return: The maximum value of the rating.
        '''
        maximum_value_rating = None
        try:
            maximum_value_rating = self.file_parser.getfloat(section='rating', option='maximum_value_rating')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return maximum_value_rating
    
    def get_even_distribution(self):
        '''
        Gets if applying an even distribution. 
        - even_distribution=True: generates a similar count of ratings by user.
        - even_distribution=False: generates a random count of ratings by user.
        :return: The boolean value.
        '''
        even_distribution = None
        try:
            even_distribution = self.file_parser.getboolean(section='rating', option='even_distribution')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return even_distribution
    
    def get_even_distribution_type(self):
        '''
        Gets the distribution type when even_distribution=False.
        :return: The distribution type.
        '''
        even_distribution_type = None
        try:
            even_distribution_type = self.file_parser.get(section='rating', option='even_distribution_type')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return even_distribution_type

    def get_percentage_rating_variation(self):
        '''
        Gets the variation percentage of the rating.
        :return: The variation percentage of the rating.
        '''
        percentage_rating_variation = None
        try:
            percentage_rating_variation = self.file_parser.getint(section='rating', option='percentage_rating_variation')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return percentage_rating_variation

    def get_all_implicit_rating_rules(self):
        '''
        Gets a list of all the implicit rating rules.
        :return: A list of dictionaries containing the details of all implicit rating rules.
        '''
        implicit_rating_rules = []
        number_maximum_rules = self.get_number_maximum_rules()
        for position in range(1, number_maximum_rules + 1):
            implicit_rating_rule = self.get_implicit_rating_rule_from_pos(position)
            if implicit_rating_rule:
                implicit_rating_rules.append(implicit_rating_rule)
        return implicit_rating_rules
    
    def get_number_maximum_rules(self):
        '''
        Gets the number of implicit rating rules.
        :return: The number of implicit rating rules.
        '''
        number_maximum_rules = None
        try:
            number_maximum_rules = self.file_parser.getint(section='rating', option='number_maximum_rules')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return number_maximum_rules
    
    def get_implicit_rating_rule_from_pos(self, position):
        '''
        Gets the details of a specific implicit rating rule.
        :param position: The position of the implicit rating rule.
        :return: The details of a specific implicit rating rule as a dictionary.
        '''
        implicit_rating_rule = None
        try:
            implicit_rating_rule_str = self.file_parser.get(section='rating', option=f'rule_{position}')
            implicit_rating_rule = ast.literal_eval(implicit_rating_rule_str)
        except (NoOptionError, NoSectionError, ValueError) as e:
            logging.error(e)
        return implicit_rating_rule

    def get_number_behavior(self):
        '''
        Gets the number of behaviors to generate in the dataset.
        :return: The number of behaviors to generate in the dataset.
        '''
        number_behavior = None
        try:
            number_behavior = self.file_parser.getint(section='behavior', option='number_behavior')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return number_behavior
    
    def get_session_time(self):
        '''
        Gets the session time to generate in the dataset.
        :return: The session time to generate in the dataset.
        '''
        session_time = None
        try:
            session_time = self.file_parser.getint(section='behavior', option='session_time')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return session_time
    
    def get_minimum_interval_behavior(self):
        '''
        Gets the minimum interval of time between two behaviors.
        :return: The minimum interval of time between two behaviors.
        '''
        minimum_interval_behavior = None
        try:
            minimum_interval_behavior = self.file_parser.getint(section='behavior', option='minimum_interval_behavior')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return minimum_interval_behavior
    
    def get_maximum_interval_behavior(self):
        '''
        Gets the maximum interval of time between two behaviors.
        :return: The maximum interval of time between two behaviors.
        '''
        maximum_interval_behavior = None
        try:
            maximum_interval_behavior = self.file_parser.getint(section='behavior', option='maximum_interval_behavior')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return maximum_interval_behavior
    
    def get_initial_position(self):
        '''
        Gets the x, y, z coordinates with the initial position (door) to generate in the virtual 3D world.
        :return: The list with the initial position
        '''
        initial_position = None
        try:
            initial_position = eval(self.file_parser.get(section='behavior', option='door'))
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return initial_position
    
    def get_minimum_radius(self):
        '''
        Gets the minimum radius of the interaction area.
        :return: The minimum radius of the interaction area.
        '''
        minimum_radius = None
        try:
            minimum_radius = self.file_parser.getint(section='behavior', option='minimum_radius')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return minimum_radius
    
    def get_maximum_radius(self):
        '''
        Gets the maximum radius of the interaction area.
        :return: The maximum radius of the interaction area.
        '''
        maximum_radius = None
        try:
            maximum_radius = self.file_parser.getint(section='behavior', option='maximum_radius')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return maximum_radius
    
    def get_interaction_threshold(self):
        '''
        Gets the interaction threshold.
        :return: The interaction threshold.
        '''
        interaction_threshold = None
        try:
            interaction_threshold = self.file_parser.getfloat(section='behavior', option='interaction_threshold')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return interaction_threshold
    
    def get_k_rating_past(self):
        '''
        Gets the k ratings to consider from a user's past to modify a specific rating.
        :return: The k ratings to consider from a user's past.
        '''
        k_rating_past = None
        try:
            k_rating_past = self.file_parser.getint(section='rating', option='k_rating_past')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return k_rating_past

    def is_gaussian_distribution(self):
        '''
        Gets if the Gaussian distribution is applied.
        :return: True if the Gaussian distribution is applied and False in the otherwise.
        '''
        is_gaussian_distribution = None
        try:
            is_gaussian_distribution = self.file_parser.getboolean(section='rating', option='gaussian_distribution')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return is_gaussian_distribution
    
    def get_minimum_date_timestamp(self):
        '''
        Gets the minimum date to generate the timestamp in the rating file.
        :return: The minimum date to generate the timestamp.
        '''
        minimum_value_rating = None
        try:
            minimum_value_rating = self.file_parser.get(section='rating', option='minimum_date_timestamp')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return minimum_value_rating
    
    def get_maximum_date_timestamp(self):
        '''
        Gets the maximum date to generate the timestamp in the rating file.
        :return: The maximum date to generate the timestamp.
        '''
        maximum_value_rating = None
        try:
            maximum_value_rating = self.file_parser.get(section='rating', option='maximum_date_timestamp')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return maximum_value_rating

    def get_probability_percentage_profile_from_pos(self, position):
        '''
        Gets the percentage to generate by item profile.
        :param position: The position of the item profile.
        :return: The percentage to generate by item profile.
        '''
        probability_percentage_profile = None
        try:
            probability_percentage_profile = self.file_parser.getint(section='item profile', option=f'probability_percentage_profile_{str(position)}')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return probability_percentage_profile

    def get_noise_percentage_profile_from_pos(self, position):
        '''
        Gets the noise percentage to generate by item profile.
        :param position: The position of the item profile.
        :return: The noise percentage to generate by item profile.
        '''
        noise_percentage_profile = None
        try:
            noise_percentage_profile = self.file_parser.getint(section='item profile', option=f'noise_percentage_profile_{str(position)}')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return noise_percentage_profile
