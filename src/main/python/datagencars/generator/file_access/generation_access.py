import logging
from configparser import NoOptionError, NoSectionError

from datagencars.generator.file_access.data_access import DataAccess


class GenerationAccess(DataAccess):
    '''
    Access to the values of the properties stored in the file generation_config.txt.
    @author Maria del Carmen Rodriguez-Hernandez 
    '''
    
    def __init__(self, file_path):
        super().__init__(file_path)
    
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

    def get_noise_percentage(self):
        '''
        Gets the noise percentage of the rating.
        :return: The noise percentage of the rating.
        '''
        noise_percentage = None
        try:
            noise_percentage = self.file_parser.getint(section='rating', option='noise_percentage')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return noise_percentage

    def is_gaussian_distribution(self):
        '''
        Gets if the Gaussian distribution is applied.
        :return: True if the Gaussian distribution is applied and False in the otherwise.
        '''
        is_gaussian_distribution = None
        try:
            is_gaussian_distribution = self.file_parser.getboolean(section='distribution', option='gaussian_distribution')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return is_gaussian_distribution
    
    def get_probability_percentage_profile_from_pos(self, position):
        '''
        Gets the percentage of users with a specific profile.
        :param position: The position of the user profile.
        :return: The percentage of users with a specific profile.
        '''
        probability_percentage_profile = None
        try:
            probability_percentage_profile = self.file_parser.getint(section='probability', option=f'probability_percentage_profile_{str(position)}')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return probability_percentage_profile

    def get_noise_percentage_profile_from_pos(self, position):
        '''
        Gets the noise percentage by user profile.
        :param position: The position of the user profile.
        :return: The percentage of users with a specific profile.
        '''
        noise_percentage_profile = None
        try:
            noise_percentage_profile = self.file_parser.getint(section='noise', option=f'noise_percentage_profile_{str(position)}')
        except (NoOptionError, NoSectionError) as e: 
            logging.error(e)
        return noise_percentage_profile


# generation_access = GenerationAccess(file_path='resources/data/generation_config.conf')

# number_user = generation_access.get_number_user()
# print(number_user)
# number_item = generation_access.get_number_item()
# print(number_item)
# number_context = generation_access.get_number_context()
# print(number_context)
# number_rating = generation_access.get_number_rating()
# print(number_rating)
# minimum_value_rating = generation_access.get_minimum_value_rating()
# print(minimum_value_rating)
# maximum_value_rating = generation_access.get_maximum_value_rating()
# print(maximum_value_rating)
# percentage_rating_variation = generation_access.get_percentage_rating_variation()
# print(percentage_rating_variation)
# noise_percentage = generation_access.get_noise_percentage()
# print(noise_percentage)
# is_gaussian_distribution = generation_access.is_gaussian_distribution()
# print(is_gaussian_distribution)
# probability_percentage_profile = generation_access.get_probability_percentage_profile_from_pos(position=1)
# print(probability_percentage_profile)
# noise_percentage_profile = generation_access.get_noise_percentage_profile_from_pos(position=1)
# print(noise_percentage_profile)