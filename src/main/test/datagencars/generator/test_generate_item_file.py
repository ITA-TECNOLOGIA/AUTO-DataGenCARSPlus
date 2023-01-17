import unittest
import logging

from datagencars.generator.file_generator.item_file_generator import ItemFileGenerator


class TestGenerateItemFile(unittest.TestCase):

    def setUp(self):
        # INPUT:
        generation_file_path = 'resources/data/generation_config.conf'
        item_schema_file_path = 'resources/data/item_schema.conf'
        item_profile_file_path = 'resources/data/item_profile.conf'
        self.__generator = ItemFileGenerator(generation_file_path, item_schema_file_path, item_profile_file_path)
    
    def tearDown(self):
        del self.__generator
    
    def test_generate_item_file_correlation(self):
        '''        
        Generates the item file with correlation.        
        '''
        logging.info('test_generate_item_file_correlation')        
        # OUTPUT:        
        item_file_df = self.__generator.generate_file(with_correlation=True)
        # print(item_file_df)
        column_name_list = item_file_df.columns.tolist()
        # print(column_name_list)
        logging.info(f'column names: {column_name_list}')
        self.assertEqual(column_name_list, ['item_id', 'web_name', 'address', 'province', 'country', 'phone', 'weekday_is_open', 'hour', 'type_of_food', 'card', 'outside', 'bar', 'parking', 'reservation', 'price', 'quality_food', 'quality_service', 'quality_price', 'global_rating'])        

    def test_generate_item_file(self):
        '''        
        Generates the item file without correlation.        
        '''
        logging.info('test_generate_item_file') 
        # OUTPUT:        
        item_file_df = self.__generator.generate_file(with_correlation=False)
        print(item_file_df)
        column_name_list = item_file_df.columns.tolist()
        # print(column_name_list)
        logging.info(f'column names: {column_name_list}')
        self.assertEqual(column_name_list, ['item_id', 'web_name', 'address', 'province', 'country', 'phone', 'weekday_is_open', 'hour', 'type_of_food', 'card', 'outside', 'bar', 'parking', 'reservation', 'price', 'quality_food', 'quality_service', 'quality_price', 'global_rating'])        

    
if __name__ == '__main__':
    unittest.main()