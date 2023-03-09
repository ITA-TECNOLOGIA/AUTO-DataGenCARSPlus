import unittest
import logging

from datagencars.synthetic_dataset.generator.access_schema.access_generation_config import AccessGenerationConfig


class TestAccessGenerationConfig(unittest.TestCase):

    def setUp(self):        
        generation_config_file_path = 'resources/data_schema/generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()            
        self.__access = AccessGenerationConfig(file_str=generation_config)
    
    def tearDown(self):
        del self.__access
    
    def test_get_number_user(self):
        '''
        [dimension]
        number_user=100
        '''
        number_user = self.__access.get_number_user()
        logging.info(f'number_user: {number_user}')                
        self.assertEqual(number_user, 100)

    def test_get_number_item(self):
        '''
        [dimension]
        number_item=1000
        '''
        number_item = self.__access.get_number_item()
        logging.info(f'number_item: {number_item}')                
        self.assertEqual(number_item, 1000)

    def test_get_number_context(self):
        '''
        [dimension]
        number_context=1500
        '''
        number_context = self.__access.get_number_context()
        logging.info(f'number_context: {number_context}')                
        self.assertEqual(number_context, 1500)

    def test_get_number_rating(self):
        '''
        [rating]
        number_rating=2000
        '''
        number_rating = self.__access.get_number_rating()
        logging.info(f'number_rating: {number_rating}')                
        self.assertEqual(number_rating, 2000)

    def test_get_minimum_value_rating(self):
        '''
        [rating]
        minimum_value_rating=1
        '''
        minimum_value_rating = self.__access.get_minimum_value_rating()
        logging.info(f'minimum_value_rating: {minimum_value_rating}')                
        self.assertEqual(minimum_value_rating, 1)

    def test_get_maximum_value_rating(self):
        '''
        [rating]
        maximum_value_rating=5
        '''
        maximum_value_rating = self.__access.get_maximum_value_rating()
        logging.info(f'maximum_value_rating: {maximum_value_rating}')                
        self.assertEqual(maximum_value_rating, 5)

    def test_get_percentage_rating_variation(self):
        '''
        [rating]
        percentage_rating_variation=25
        '''
        percentage_rating_variation = self.__access.get_percentage_rating_variation()
        logging.info(f'percentage_rating_variation: {percentage_rating_variation}')                
        self.assertEqual(percentage_rating_variation, 25)

    def test_get_k_rating_past(self):
        '''
        [rating]
        k_rating_past=10
        '''
        k_rating_past = self.__access.get_k_rating_past()
        logging.info(f'k_rating_past: {k_rating_past}')                
        self.assertEqual(k_rating_past, 10)

    def test_is_gaussian_distribution(self):
        '''
        [rating]
        gaussian_distribution=False
        '''
        gaussian_distribution = self.__access.is_gaussian_distribution()
        logging.info(f'gaussian_distribution: {gaussian_distribution}')                
        self.assertEqual(bool(gaussian_distribution), False)

    def test_get_minimum_year_timestamp(self):
        '''
        [rating]
        minimum_year_timestamp=1980
        '''
        minimum_year_timestamp = self.__access.get_minimum_year_timestamp()
        logging.info(f'minimum_year_timestamp: {minimum_year_timestamp}')                
        self.assertEqual(minimum_year_timestamp, 1980)

    def test_get_maximum_year_timestamp(self):
        '''
        [rating]
        maximum_year_timestamp=2022
        '''
        maximum_year_timestamp = self.__access.get_maximum_year_timestamp()
        logging.info(f'maximum_year_timestamp: {maximum_year_timestamp}')                
        self.assertEqual(maximum_year_timestamp, 2022)

    def test_get_probability_percentage_profile_from_pos(self):
        '''
        [item profile]
        probability_percentage_profile_1=10
        probability_percentage_profile_2=30
        probability_percentage_profile_3=60
        '''
        probability_percentage_profile_from_pos_1 = self.__access.get_probability_percentage_profile_from_pos(position=1)
        logging.info(f'probability_percentage_profile_from_pos_1: {probability_percentage_profile_from_pos_1}')                
        self.assertEqual(probability_percentage_profile_from_pos_1, 10)

    def test_get_noise_percentage_profile_from_pos(self):
        '''
        [item profile]
        noise_percentage_profile_1=20
        noise_percentage_profile_2=20
        noise_percentage_profile_3=20
        '''
        noise_percentage_profile_from_pos_1 = self.__access.get_noise_percentage_profile_from_pos(position=1)
        logging.info(f'noise_percentage_profile_from_pos_1: {noise_percentage_profile_from_pos_1}')                
        self.assertEqual(noise_percentage_profile_from_pos_1, 20)


if __name__ == '__main__':
    unittest.main()
