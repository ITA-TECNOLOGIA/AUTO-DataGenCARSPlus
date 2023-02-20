import logging
import random

from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute import GeneratorAttribute
import numpy as np


class GeneratorAttributeGaussian(GeneratorAttribute):
    '''
    A generator of attribute values following a gaussian distribution: an integer or float value in a given range, a string value from an enumerated list, or a boolean value.

    @author Maria del Carmen Rodriguez-Hernandez
    '''
    
    def __init__(self, schema_access):
        super().__init__(schema_access)

    def generate_attribute_value(self, position):
        # sourcery skip: extract-duplicate-method, extract-method, inline-immediately-returned-variable
        '''
        Generates an attribute value (random by using a gaussian -normal- distribution) of a instance.

        Example of context_schema.conf:
            [attribute1]
            name_attribute_1=transport_way
            type_attribute_1=String
            number_posible_values_attribute_1=4
            posible_value_1_attribute_1=walking
            posible_value_2_attribute_1=bicycle
            posible_value_3_attribute_1=car
            posible_value_4_attribute_1=public
            generator_type_attribute_1=RandomAttributeGenerator
            important_weight_attribute_1=true
        :param position: The position of an attribute.
        :return: The attribute value (random). 
        '''
        attribute_value = None
        attribute_name = self.schema_access.get_attribute_name_from_pos(position)
        if attribute_name == 'user_profile_id':
            print('TODO')
        else:            
            type_attribute = self.schema_access.get_type_attribute_from_pos(position)            
            if type_attribute in ['Integer', 'Float']:
                minimum_value = self.schema_access.get_minimum_value_attribute_from_pos(position)
                maximum_value = self.schema_access.get_maximum_value_attribute_from_pos(position)
                if type_attribute == 'Integer':
                    # Generating a list of int values.   
                    array_np = np.array(list(range(int(minimum_value), int(maximum_value)+1)))
                elif type_attribute == 'Float':
                    # Generating a list of float values with 0.1 increment.
                    array_np = np.arange(float(minimum_value), float(maximum_value)+0.1, 0.1)
                # Determining the mean and standard deviation to generate an attribute value following a Gaussian distribution:
                mean = np.mean(array_np)
                standard_deviation = np.std(array_np)
                attribute_value = int(random.gauss(mu=mean, sigma=standard_deviation))                 
            elif type_attribute == 'String':            
                possible_values_attribute_list = self.schema_access.get_possible_values_attribute_list_from_pos(position)
                # Selecting one element from a str list following the normal (gauss) distribution.
                attribute_value = self.normal_choice(lst=possible_values_attribute_list)            
            elif type_attribute == 'Boolean':
                # Selecting one element from a boolean list following the normal (gauss) distribution.              
                attribute_value = self.normal_choice(lst=[True, False])   
        return attribute_name, attribute_value

    def normal_choice(self, lst, mu=None, sigma=None):
        '''
        Select one element from a str list following the normal (gauss) distribution.
        :param lst: The list.
        :param mean: The mean.
        :param sigma: The standard deviation.
        :return: One element from a str list following the normal distribution.  
        '''
        if mu is None:
            # if mu (mean) is not specified, use center of list
            mu = (len(lst)-1)/2
        if sigma is None:
            # if sigma (standard deviation) is not specified, let list be -3 .. +3 standard deviations
            sigma = len(lst)/6
        while True:
            index = int(random.normalvariate(mu, sigma) + 0.5)
            if 0 <= index < len(lst):
                return lst[index]

# from datagencars.generator.file_access.schema_access import SchemaAccess
# schema_access = SchemaAccess(file_path='resources/data/user_schema.conf')
# gaussian_attribute_generator = GaussianAttributeGenerator(schema_access)
# attribute_name, attribute_value_list = gaussian_attribute_generator.generate_attribute_value(position=1)
# print('attribute_name: ', attribute_name)
# print('attribute_value_list: ', attribute_value_list)
