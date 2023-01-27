import logging
from configparser import NoOptionError, NoSectionError

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
