import datetime
import logging
import random

from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute import GeneratorAttribute


class GeneratorAttributeDate(GeneratorAttribute):
    '''
    A generator of random dates within a certain range of dates required.
    
    Example of user_schema.conf:
        [attribute1]
        name_attribute_1=birthdate
        type_attribute_1=String
        minimum_value_attribute_1=1957
        maximum_value_attribute_1=2000
        generator_type_attribute_1=DateAttributeGenerator
 
    @author Maria del Carmen Rodriguez-Hernandez
    '''

    def __init__(self, schema_access):
        super().__init__(schema_access)

    def generate_attribute_value(self, position):
        '''
        Generates a date for an attribute. The structure of the date is dd/mm/yyyy.
        :param position: The position of an attribute.
        :return: The attribute value.
        '''
        attribute_value = None
        attribute_name = self.schema_access.get_attribute_name_from_pos(position)
        minimum_value_attribute = self.schema_access.get_minimum_value_attribute_from_pos(position)
        maximum_value_attribute = self.schema_access.get_maximum_value_attribute_from_pos(position)
        attribute_value = self.random_times(start_year=minimum_value_attribute, end_year=maximum_value_attribute)
        return attribute_name, attribute_value

    def random_times(self, start_year, end_year):
        '''
        '''
        frmt = '%d-%m-%Y'
        stime = datetime.datetime.strptime(f'1-1-{str(start_year)}', frmt)
        etime = datetime.datetime.strptime(f'1-1-{str(end_year)}', frmt)
        td = etime - stime
        date_value = random.random() * td + stime
        return f'{date_value.day}-{date_value.month}-{date_value.year}'
    

# from datagencars.generator.file_access.schema_access import SchemaAccess
# schema_access = SchemaAccess(file_path='resources/data/user_schema.conf')
# date_attribute_generator = DateAttributeGenerator(schema_access)
# attribute_name, attribute_value_list = date_attribute_generator.generate_attribute_value(position=4)
# print('attribute_name: ', attribute_name)
# print('attribute_value_list: ', attribute_value_list)

# start_year = 1957
# end_year = 2000
# date_result = date_attribute_generator.randomtimes(start_year, end_year)
# print(date_result)