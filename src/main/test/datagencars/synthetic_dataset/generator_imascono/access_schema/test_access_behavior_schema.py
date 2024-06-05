import unittest
import logging

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema
from datagencars.synthetic_dataset.generator.generator_output_file.generator_file import GeneratorFile


class TestAccessBehaviorSchema(unittest.TestCase):

    def setUp(self):        
        user_schema_file_path = 'resources/generate_synthetic_dataset/rating_implicit/context/data_schema/imascono/behavior_schema.conf'
        with open(user_schema_file_path, 'r') as user_schema_file:
            user_schema = user_schema_file.read()            
        self.__access = AccessSchema(file_str=user_schema)
    
    def tearDown(self):
        del self.__access
    
    def test_get_type(self):
        '''
        [global]
        type=behavior
        '''
        schema_type = self.__access.get_type()
        logging.info(f'type: {schema_type}')                
        self.assertEqual(schema_type, 'behavior')            

    def test_get_number_attributes(self):
        '''
        [global]
        number_attributes=8
        '''
        number_attributes = self.__access.get_number_attributes()
        logging.info(f'number_attributes: {number_attributes}')                
        self.assertEqual(number_attributes, 8)         

    def test_get_attribute_name_list(self):
        '''
        [attribute1]
        name_attribute_1=object_action_poster

        [attribute2]
        name_attribute_2=object_action_sphere

        [attribute3]
        name_attribute_3=object_action_screen

        [attribute4]
        name_attribute_4=object_action_npc

        [attribute5]
        name_attribute_5=object_action_player

        [attribute6]
        name_attribute_6=object_action_button

        [attribute7]
        name_attribute_7=user_id

        [attribute8]
        name_attribute_8=object_id
        '''
        attribute_name_list = self.__access.get_attribute_name_list()
        logging.info(f'attribute_name_list: {attribute_name_list}')          
        self.assertListEqual(attribute_name_list, ['object_action_poster', 'object_action_sphere', 'object_action_screen', 'object_action_npc', 'object_action_player', 'object_action_button', 'user_id', 'object_id'])

    def test_get_attribute_name_from_pos(self):
        '''
        [attribute1]
        name_attribute_1=object_action_poster
        '''
        attribute_name = self.__access.get_attribute_name_from_pos(position=1)
        logging.info(f'name_attribute_1: {attribute_name}')          
        self.assertEqual(attribute_name, 'object_action_poster')   

    def test_get_position_from_attribute_name(self):
        '''
        [attribute1]
        name_attribute_1=object_action_poster
        '''
        position = self.__access.get_position_from_attribute_name(attribute_name='object_action_poster')
        logging.info(f'name_attribute_1: {position}')     
        self.assertEqual(position, 1)       

    def test_get_type_attribute_from_pos(self):
        '''
        [attribute1]        
        type_attribute_1=String
        '''
        type_attribute = self.__access.get_type_attribute_from_pos(position=1)
        logging.info(f'type_attribute: {type_attribute}')          
        self.assertEqual(type_attribute, 'String')

    def test_get_generator_type_attribute_from_pos(self):
        '''
        [attribute1]        
        generator_type_attribute_1=RandomAttributeGenerator
        '''
        generator_type = self.__access.get_generator_type_attribute_from_pos(position=1)
        logging.info(f'generator_type: {generator_type}')          
        self.assertEqual(generator_type, 'RandomAttributeGenerator')

    def test_get_number_posible_values_attribute_from_pos(self):
        '''
        [attribute1]
        number_posible_values_attribute_1=3
        '''
        number_posible_values = self.__access.get_number_posible_values_attribute_from_pos(position=1)
        logging.info(f'number_posible_values: {number_posible_values}')          
        self.assertEqual(number_posible_values, 3)

    def test_get_possible_values_attribute_list_from_pos(self):
        '''
        [attribute1]
        posible_value_1_attribute_1=Open
        posible_value_2_attribute_1=Click
        posible_value_3_attribute_1=Close
        '''
        possible_values = self.__access.get_possible_values_attribute_list_from_pos(position=1)
        logging.info(f'possible_values: {possible_values}')          
        self.assertListEqual(possible_values, ['Open', 'Click', 'Close'])

    def test_get_possible_values_attribute_list_from_name_other(self):
        '''
        It is an attribute of the user's profile, but not of the user.
        '''
        possible_values = self.__access.get_possible_values_attribute_list_from_name(attribute_name='other')
        logging.info(f'possible_values: {possible_values}') 
        self.assertListEqual(possible_values, [])

if __name__ == '__main__':
    unittest.main()
