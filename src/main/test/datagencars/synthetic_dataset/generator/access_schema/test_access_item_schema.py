import unittest
import logging

from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema


class TestAccessItemSchema(unittest.TestCase):

    def setUp(self):        
        user_schema_file_path = 'resources/data_schema/item_schema.conf'
        with open(user_schema_file_path, 'r') as user_schema_file:
            user_schema = user_schema_file.read()            
        self.__access = AccessSchema(file_str=user_schema)
    
    def tearDown(self):
        del self.__access
    
    def test_get_type(self):
        '''
        [global]
        type=item
        '''
        schema_type = self.__access.get_type()
        logging.info(f'type: {schema_type}')                
        self.assertEqual(schema_type, 'item')            

    def test_get_number_attributes(self):
        '''
        [global]
        number_attributes=4
        '''
        number_attributes = self.__access.get_number_attributes()
        logging.info(f'number_attributes: {number_attributes}')                
        self.assertEqual(number_attributes, 18)         

    def test_get_attribute_name_list(self):
        '''
        [attribute1]
        name_attribute_1=web_name

        [attribute2]
        name_attribute_2=address

        [attribute3]
        name_attribute_3=province

        [attribute4]
        name_attribute_4=country

        [attribute5]
        name_attribute_5=phone

        [attribute6]
        name_attribute_6=weekday_is_open

        [attribute7]
        name_attribute_7=hour

        [attribute8]
        name_attribute_8=type_of_food

        [attribute9]
        name_attribute_9=card

        [attribute10]
        name_attribute_10=outside

        [attribute11]
        name_attribute_11=bar

        [attribute12]
        name_attribute_12=parking

        [attribute13]
        name_attribute_13=reservation

        [attribute14]
        name_attribute_14=price

        [attribute15]
        name_attribute_15=quality_food

        [attribute16]
        name_attribute_16=quality_service

        [attribute17]
        name_attribute_17=quality_price

        [attribute18]
        name_attribute_18=global_rating
        '''
        attribute_name_list = self.__access.get_attribute_name_list()
        logging.info(f'attribute_name_list: {attribute_name_list}')          
        self.assertListEqual(attribute_name_list, ['web_name', 'address', 'province', 'country', 'phone', 'weekday_is_open', 'hour', 'type_of_food', 'card', 'outside', 'bar', 'parking', 'reservation', 'price', 'quality_food', 'quality_service', 'quality_price', 'global_rating'])

    def test_get_attribute_name_from_pos(self):
        '''
        [attribute1]
        name_attribute_1=web_name
        '''
        attribute_name = self.__access.get_attribute_name_from_pos(position=1)
        logging.info(f'name_attribute_1: {attribute_name}')          
        self.assertEqual(attribute_name, 'web_name')   

    def test_get_position_from_attribute_name(self):
        '''
        [attribute1]
        name_attribute_1=web_name
        '''
        position = self.__access.get_position_from_attribute_name(attribute_name='web_name')
        logging.info(f'name_attribute_1: {position}')          
        self.assertEqual(position, 1)       

    def test_get_type_attribute_from_pos(self):
        '''
        [attribute1]        
        type_attribute_1=AttributeComposite
        '''
        type_attribute = self.__access.get_type_attribute_from_pos(position=1)
        logging.info(f'type_attribute: {type_attribute}')          
        self.assertEqual(type_attribute, 'AttributeComposite')

    def test_get_generator_type_attribute_from_pos(self):
        '''
        [attribute1]        
        generator_type_attribute_1=URLAttributeGenerator
        '''
        generator_type = self.__access.get_generator_type_attribute_from_pos(position=1)
        logging.info(f'generator_type: {generator_type}')          
        self.assertEqual(generator_type, 'URLAttributeGenerator')

    def test_get_number_posible_values_attribute_from_pos(self):
        '''
        [attribute14]
        number_posible_values_attribute_14=5
        '''
        number_posible_values = self.__access.get_number_posible_values_attribute_from_pos(position=14)
        logging.info(f'number_posible_values: {number_posible_values}')          
        self.assertEqual(number_posible_values, 5)

    def test_get_possible_values_attribute_list_from_pos(self):
        '''
        [attribute14]
        posible_value_1_attribute_14=free
        posible_value_2_attribute_14=$
        posible_value_3_attribute_14=$$
        posible_value_4_attribute_14=$$$
        posible_value_5_attribute_14=$$$$
        '''
        possible_values = self.__access.get_possible_values_attribute_list_from_pos(position=14)
        logging.info(f'possible_values: {possible_values}')          
        self.assertListEqual(possible_values, ['free', '$', '$$', '$$$', '$$$$'])

    def test_get_input_parameter_attribute_from_pos(self):
        '''
        [attribute1]
        input_parameter_attribute_1=name_restaurant.csv
        '''
        input_parameter = self.__access.get_input_parameter_attribute_from_pos(position=1)
        logging.info(f'input_parameter: {input_parameter}')          
        self.assertEqual(input_parameter, 'name_restaurant.csv')

    def test_get_minimum_value_attribute_from_pos(self):
        '''
        [attribute18]
        minimum_value_attribute_18=1        
        '''
        minimum_value = self.__access.get_minimum_value_attribute_from_pos(position=18)
        logging.info(f'minimum_value: {minimum_value}')          
        self.assertEqual(int(minimum_value), 1)

    def test_get_maximum_value_attribute_from_pos(self):
        '''
        [attribute18]
        maximum_value_attribute_18=5
        '''
        maximum_value = self.__access.get_maximum_value_attribute_from_pos(position=18)
        logging.info(f'maximum_value: {maximum_value}')          
        self.assertEqual(int(maximum_value), 5)

    def test_get_number_maximum_component_attribute_from_pos(self):
        '''
        [attribute6]        
        number_maximum_component_attribute_6=7
        '''
        number_maximum_component = self.__access.get_number_maximum_component_attribute_from_pos(position=6)
        logging.info(f'number_maximum_component: {number_maximum_component}')          
        self.assertEqual(int(number_maximum_component), 7)
        
    def test_get_type_component_attribute_from_pos(self):
        '''
        [attribute6]
        type_component_attribute_6=Boolean
        '''
        type_component = self.__access.get_type_component_attribute_from_pos(position=6)
        logging.info(f'type_component: {type_component}')          
        self.assertEqual(type_component, 'Boolean')

    def test_get_component_attribute_list_from_pos(self):
        '''
        [attribute6]
        component_1_attribute_6=monday
        component_2_attribute_6=tuesday
        component_3_attribute_6=wednesday
        component_4_attribute_6=thursday
        component_5_attribute_6=friday
        component_6_attribute_6=saturday
        component_7_attribute_6=sunday
        '''
        component_attribute_list = self.__access.get_component_attribute_list_from_pos(position=6)
        logging.info(f'component_attribute_list: {component_attribute_list}')          
        self.assertListEqual(component_attribute_list, ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])

    def test_get_number_maximum_subattribute_from_pos(self):
        '''
        [attribute2]        
        number_maximum_subattribute_attribute_2=5
        '''
        number_maximum_subattribute = self.__access.get_number_maximum_subattribute_from_pos(position=2)
        logging.info(f'number_maximum_subattribute: {number_maximum_subattribute}')          
        self.assertEqual(number_maximum_subattribute, 5)

    def test_get_name_subattribute_list_from_pos(self):
        '''
        [attribute2]
        name_subattribute_1_attribute_2=street
        name_subattribute_2_attribute_2=number
        name_subattribute_3_attribute_2=zp
        name_subattribute_4_attribute_2=latitude
        name_subattribute_5_attribute_2=longitude
        '''
        name_subattribute_list = self.__access.get_name_subattribute_list_from_pos(position=2)
        logging.info(f'name_subattribute_list: {name_subattribute_list}')          
        self.assertListEqual(name_subattribute_list, ['street', 'number', 'zp', 'latitude', 'longitude'])

    def test_get_name_subattribute_from_pos(self):
        '''
        [attribute2]
        name_subattribute_1_attribute_2=street   
        '''
        name_subattribute = self.__access.get_name_subattribute_from_pos(position_attribute=2, position_subattribute=1)
        logging.info(f'name_subattribute: {name_subattribute}')          
        self.assertEqual(name_subattribute, 'street')    

    def test_get_type_subattribute_from_pos(self):
        '''
        [attribute2]        
        type_subattribute_1_attribute_2=String        
        '''
        type_subattribute = self.__access.get_type_subattribute_from_pos(position_attribute=2, position_subattribute=1)
        logging.info(f'type_subattribute: {type_subattribute}')          
        self.assertEqual(type_subattribute, 'String')

    def test_get_important_profile_attribute_from_pos(self):
        '''
        [attribute15]        
        important_profile_attribute_15=True      
        '''
        important_profile = self.__access.get_important_profile_attribute_from_pos(position=15)
        logging.info(f'important_profile: {important_profile}')          
        self.assertEqual(bool(important_profile), True)

    def test_get_ranking_order_by_attribute_from_pos(self):
        '''
        [attribute15]
        ranking_order_by_attribute_15=desc  
        '''
        ranking_order = self.__access.get_ranking_order_by_attribute_from_pos(position=15)
        logging.info(f'ranking_order: {ranking_order}')          
        self.assertEqual(ranking_order, 'desc')

    def test_get_number_important_weight_attribute(self):
        '''
        [attribute8]
        important_weight_attribute_8=True

        [attribute9]
        important_weight_attribute_9=True

        [attribute10]
        important_weight_attribute_10=True

        [attribute11]
        important_weight_attribute_11=True

        [attribute12]
        important_weight_attribute_12=True

        [attribute13]
        important_weight_attribute_13=True

        [attribute14]
        important_weight_attribute_14=True

        [attribute15]
        important_weight_attribute_15=True

        [attribute16]
        important_weight_attribute_16=True

        [attribute17]
        important_weight_attribute_17=True

        [attribute18]
        important_weight_attribute_18=True
        '''
        number_important_weight = self.__access.get_number_important_weight_attribute()
        logging.info(f'number_important_weight: {number_important_weight}')          
        self.assertEqual(number_important_weight, 11)

    def test_get_important_weight_attribute_from_pos(self):
        '''
        [attribute8]
        important_weight_attribute_8=True        
        '''
        important_weight = self.__access.get_important_weight_attribute_from_pos(position=8)
        logging.info(f'important_weight: {important_weight}')          
        self.assertEqual(bool(important_weight), True)        


if __name__ == '__main__':
    unittest.main()
