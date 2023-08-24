import unittest
import logging

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema


class TestAccessUserSchema(unittest.TestCase):

    def setUp(self):        
        user_schema_file_path = 'resources/generate_synthetic_dataset/rating_explicit/context/restaurant/data_schema/user_schema.conf'
        with open(user_schema_file_path, 'r') as user_schema_file:
            user_schema = user_schema_file.read()            
        self.__access = AccessSchema(file_str=user_schema)
    
    def tearDown(self):
        del self.__access
    
    def test_get_type(self):
        '''
        [global]
        type=user
        '''
        schema_type = self.__access.get_type()
        logging.info(f'type: {schema_type}')                
        self.assertEqual(schema_type, 'user')            

    def test_get_number_attributes(self):
        '''
        [global]
        number_attributes=5
        '''
        number_attributes = self.__access.get_number_attributes()
        logging.info(f'number_attributes: {number_attributes}')                
        self.assertEqual(number_attributes, 5)         

    def test_get_attribute_name_list(self):
        '''
        [attribute1]
        name_attribute_1=age

        [attribute2]
        name_attribute_2=gender

        [attribute3]
        name_attribute_3=occupation

        [attribute4]
        name_attribute_4=birthdate

        [attribute5]
        name_attribute_5=user_profile_id
        '''
        attribute_name_list = self.__access.get_attribute_name_list()
        logging.info(f'attribute_name_list: {attribute_name_list}')          
        self.assertListEqual(attribute_name_list, ['age', 'gender', 'occupation', 'birthdate', 'user_profile_id'])        

    def test_get_attribute_name_from_pos(self):
        '''
        [attribute1]
        name_attribute_1=age
        '''
        attribute_name = self.__access.get_attribute_name_from_pos(position=1)
        logging.info(f'name_attribute_1: {attribute_name}')          
        self.assertEqual(attribute_name, 'age')        

    def test_get_type_attribute_from_pos(self):
        '''
        [attribute1]        
        type_attribute_1=Integer
        '''
        type_attribute = self.__access.get_type_attribute_from_pos(position=1)
        logging.info(f'type_attribute: {type_attribute}')          
        self.assertEqual(type_attribute, 'Integer')

    def test_get_generator_type_attribute_from_pos(self):
        '''
        [attribute3]        
        generator_type_attribute_3=RandomAttributeGenerator
        '''
        generator_type = self.__access.get_generator_type_attribute_from_pos(position=3)
        logging.info(f'generator_type: {generator_type}')          
        self.assertEqual(generator_type, 'RandomAttributeGenerator')

    def test_get_number_posible_values_attribute_from_pos(self):
        '''
        [attribute2]
        number_posible_values_attribute_2=2
        '''
        number_posible_values = self.__access.get_number_posible_values_attribute_from_pos(position=2)
        logging.info(f'number_posible_values: {number_posible_values}')          
        self.assertEqual(number_posible_values, 2)

    def test_get_possible_values_attribute_list_from_pos(self):
        '''
        [attribute2]
        posible_value_1_attribute_2=female
        posible_value_2_attribute_2=male
        '''
        possible_values = self.__access.get_possible_values_attribute_list_from_pos(position=2)
        logging.info(f'possible_values: {possible_values}')          
        self.assertListEqual(possible_values, ['female', 'male'])

    def test_get_minimum_value_attribute_from_pos(self):
        '''
        [attribute1]
        minimum_value_attribute_1=18
        '''
        minimum_value = self.__access.get_minimum_value_attribute_from_pos(position=1)
        logging.info(f'minimum_value: {minimum_value}')          
        self.assertEqual(int(minimum_value), 18)

    def test_get_maximum_value_attribute_from_pos(self):
        '''
        [attribute1]
        maximum_value_attribute_1=80
        '''
        maximum_value = self.__access.get_maximum_value_attribute_from_pos(position=1)
        logging.info(f'maximum_value: {maximum_value}')          
        self.assertEqual(int(maximum_value), 80)


if __name__ == '__main__':
    unittest.main()
