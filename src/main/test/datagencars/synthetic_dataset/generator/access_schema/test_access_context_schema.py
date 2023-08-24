import unittest
import logging

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema


class TestAccessContextSchema(unittest.TestCase):

    def setUp(self):        
        context_schema_file_path = 'resources/generate_synthetic_dataset/rating_explicit/context/restaurant/data_schema/context_schema.conf'
        with open(context_schema_file_path, 'r') as context_schema_file:
            context_schema = context_schema_file.read()            
        self.__access = AccessSchema(file_str=context_schema)
    
    def tearDown(self):
        del self.__access
    
    def test_get_type(self):
        '''
        [global]
        type=context
        '''
        schema_type = self.__access.get_type()
        logging.info(f'type: {schema_type}')                
        self.assertEqual(schema_type, 'context')            

    def test_get_number_attributes(self):
        '''
        [global]
        number_attributes=7
        '''
        number_attributes = self.__access.get_number_attributes()
        logging.info(f'number_attributes: {number_attributes}')                
        self.assertEqual(number_attributes, 7)         

    def test_get_attribute_name_list(self):
        '''
        [attribute1]
        name_attribute_1=transport_way

        [attribute2]
        name_attribute_2=mobility

        [attribute3]
        name_attribute_3=weekday

        [attribute4]
        name_attribute_4=mood

        [attribute5]
        name_attribute_5=companion

        [attribute6]
        name_attribute_6=time_of_day

        [attribute7]
        name_attribute_7=distance
        '''
        attribute_name_list = self.__access.get_attribute_name_list()
        logging.info(f'attribute_name_list: {attribute_name_list}')          
        self.assertListEqual(attribute_name_list, ['transport_way', 'mobility', 'weekday', 'mood', 'companion', 'time_of_day', 'distance'])

    def test_get_attribute_name_from_pos(self):
        '''
        [attribute1]
        name_attribute_1=transport_way
        '''
        attribute_name = self.__access.get_attribute_name_from_pos(position=1)
        logging.info(f'name_attribute_1: {attribute_name}')          
        self.assertEqual(attribute_name, 'transport_way')   

    def test_get_position_from_attribute_name(self):
        '''
        [attribute1]
        name_attribute_1=transport_way
        '''
        position = self.__access.get_position_from_attribute_name(attribute_name='transport_way')
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
        number_posible_values_attribute_1=4
        '''
        number_posible_values = self.__access.get_number_posible_values_attribute_from_pos(position=1)
        logging.info(f'number_posible_values: {number_posible_values}')          
        self.assertEqual(number_posible_values, 4)

    def test_get_possible_values_attribute_list_from_pos(self):
        '''
        [attribute1]
        posible_value_1_attribute_1=walking
        posible_value_2_attribute_1=bicycle
        posible_value_3_attribute_1=car
        posible_value_4_attribute_1=public
        '''
        possible_values = self.__access.get_possible_values_attribute_list_from_pos(position=1)
        logging.info(f'possible_values: {possible_values}')          
        self.assertListEqual(possible_values, ['walking', 'bicycle', 'car', 'public'])

    def test_get_possible_values_attribute_list_from_name_str(self):
        '''
        [attribute1]
        name_attribute_1=transport_way
        posible_value_1_attribute_1=walking
        posible_value_2_attribute_1=bicycle
        posible_value_3_attribute_1=car
        posible_value_4_attribute_1=public
        '''
        possible_values = self.__access.get_possible_values_attribute_list_from_name(attribute_name='transport_way')
        logging.info(f'possible_values: {possible_values}')          
        self.assertListEqual(possible_values, ['walking', 'bicycle', 'car', 'public'])

    def test_get_possible_values_attribute_list_from_name_other(self):
        '''
        It is an attribute of the user's profile, but not of the user.
        '''
        possible_values = self.__access.get_possible_values_attribute_list_from_name(attribute_name='other')
        logging.info(f'possible_values: {possible_values}') 
        self.assertListEqual(possible_values, [])

    def test_get_number_important_weight_attribute(self):
        '''
        [attribute1]
        important_weight_attribute_1=True

        [attribute2]
        important_weight_attribute_2=True

        [attribute3]
        important_weight_attribute_3=Truec

        [attribute4]
        important_weight_attribute_4=True

        [attribute5]
        important_weight_attribute_5=True

        [attribute6]
        important_weight_attribute_6=True

        [attribute7]
        important_weight_attribute_7=True
        '''
        number_important_weight = self.__access.get_number_important_weight_attribute()
        logging.info(f'number_important_weight: {number_important_weight}')          
        self.assertEqual(number_important_weight, 7)

    def test_get_important_weight_attribute_from_pos(self):
        '''
        [attribute1]
        important_weight_attribute_1=True
        '''
        important_weight = self.__access.get_important_weight_attribute_from_pos(position=1)
        logging.info(f'important_weight: {important_weight}')          
        self.assertEqual(bool(important_weight), True)  

    def test_get_important_attribute_name_list(self):
        '''
        [attribute1]
        name_attribute_1=transport_way
        important_weight_attribute_1=True

        [attribute2]
        name_attribute_2=mobility        
        important_weight_attribute_2=True

        [attribute3]
        name_attribute_3=weekday        
        important_weight_attribute_3=True

        [attribute4]
        name_attribute_4=mood        
        important_weight_attribute_4=True

        [attribute5]
        name_attribute_5=companion        
        important_weight_attribute_5=True

        [attribute6]
        name_attribute_6=time_of_day        
        important_weight_attribute_6=True

        [attribute7]
        name_attribute_7=distance        
        important_weight_attribute_7=True
        '''
        important_attribute_name_list = self.__access.get_important_attribute_name_list()          
        logging.info(f'important_attribute_name_list: {important_attribute_name_list}')          
        self.assertListEqual(important_attribute_name_list, ['transport_way', 'mobility', 'weekday', 'mood', 'companion', 'time_of_day', 'distance'])      


if __name__ == '__main__':
    unittest.main()
