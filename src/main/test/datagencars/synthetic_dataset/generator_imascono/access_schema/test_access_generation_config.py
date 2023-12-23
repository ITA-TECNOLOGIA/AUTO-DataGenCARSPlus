import datetime
import unittest
import logging

from datagencars.synthetic_dataset.generator.access_schema.access_generation_config import AccessGenerationConfig


class TestAccessGenerationConfig(unittest.TestCase):

    def setUp(self):        
        generation_config_file_path = 'resources/data_schema_imascono/generation_config.conf'
        with open(generation_config_file_path, 'r') as generation_config_file:
            generation_config = generation_config_file.read()            
        self.__access = AccessGenerationConfig(file_str=generation_config)
    
    def tearDown(self):
        del self.__access
    
    def test_get_number_user(self):
        '''
        [dimension]
        number_user=13810
        '''
        number_user = self.__access.get_number_user()
        logging.info(f'number_user: {number_user}')                
        self.assertEqual(number_user, 13810)

    def test_get_number_item(self):
        '''
        [dimension]
        number_item=36
        '''
        number_item = self.__access.get_number_item()
        logging.info(f'number_item: {number_item}')                
        self.assertEqual(number_item, 36)

    def test_get_number_context(self):
        '''
        [dimension]
        number_context=11130
        '''
        number_context = self.__access.get_number_context()
        logging.info(f'number_context: {number_context}')                
        self.assertEqual(number_context, 11130)

    def test_get_minimum_value_rating(self):
        '''
        [rating]
        minimum_value_rating=0
        '''
        minimum_value_rating = self.__access.get_minimum_value_rating()
        logging.info(f'minimum_value_rating: {minimum_value_rating}')                
        self.assertEqual(minimum_value_rating, 0)

    def test_get_maximum_value_rating(self):
        '''
        [rating]
        maximum_value_rating=1
        '''
        maximum_value_rating = self.__access.get_maximum_value_rating()
        logging.info(f'maximum_value_rating: {maximum_value_rating}')                
        self.assertEqual(maximum_value_rating, 1)

    def test_get_minimum_date_timestamp(self):
        '''
        [rating]
        minimum_date_timestamp=2023-01-01
        '''
        minimum_date_timestamp = self.__access.get_minimum_date_timestamp()
        logging.info(f'minimum_date_timestamp: {minimum_date_timestamp}')                
        self.assertEqual(minimum_date_timestamp, "2023-01-01")

    def test_get_maximum_date_timestamp(self):
        '''
        [rating]
        maximum_date_timestamp=2023-04-01
        '''
        maximum_date_timestamp = self.__access.get_maximum_date_timestamp()
        logging.info(f'maximum_date_timestamp: {maximum_date_timestamp}')                
        self.assertEqual(maximum_date_timestamp, "2023-04-01")

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

    def test_get_number_behavior(self):
        '''
        [behavior]
        number_behavior=5
        '''
        number_behavior = self.__access.get_number_behavior()
        logging.info(f'number_behavior: {number_behavior}')                
        self.assertEqual(number_behavior, 18500)

    def test_get_session_time(self):
        '''
        [behavior]
        session_time=120
        '''
        session_time = self.__access.get_session_time()
        logging.info(f'session_time: {session_time}')                
        self.assertEqual(session_time, 3600)

    def test_get_minimum_interval_behavior(self):
        '''
        [behavior]
        minimum_interval_behavior=5
        '''
        minimum_interval_behavior = self.__access.get_minimum_interval_behavior()
        logging.info(f'minimum_interval_behavior: {minimum_interval_behavior}')                
        self.assertEqual(minimum_interval_behavior, 1)

    def test_get_maximum_interval_behavior(self):
        '''
        [behavior]
        maximum_interval_behavior=30
        '''
        maximum_interval_behavior = self.__access.get_maximum_interval_behavior()
        logging.info(f'maximum_interval_behavior: {maximum_interval_behavior}')                
        self.assertEqual(maximum_interval_behavior, 300)

if __name__ == '__main__':
    unittest.main()
