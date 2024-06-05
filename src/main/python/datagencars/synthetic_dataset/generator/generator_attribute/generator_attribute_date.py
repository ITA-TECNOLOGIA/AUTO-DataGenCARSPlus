import datetime
import logging
import random

from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute import GeneratorAttribute


class GeneratorAttributeDate(GeneratorAttribute):
    '''
    A generator of random dates within a certain range of dates required.
    
    Example of user_schema.conf:
        [attribute4]
        name_attribute_4=birthdate
        type_attribute_4=String
        minimum_value_attribute_4=1957
        maximum_value_attribute_4=2000
        generator_type_attribute_4=DateAttributeGenerator
 
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
