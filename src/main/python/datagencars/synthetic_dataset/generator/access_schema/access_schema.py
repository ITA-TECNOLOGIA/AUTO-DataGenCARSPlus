import logging
from configparser import NoOptionError, NoSectionError
import numpy as np

from datagencars.synthetic_dataset.generator.access_schema.access_data import AccessData


class AccessSchema(AccessData):
    '''
    Gets the values of the properties stored in a schema file (user_schema.txt, item_schema.txt or context_schema.txt). 
    @author Maria del Carmen Rodriguez-Hernandez 
    '''

    def __init__(self, file_str):
        super().__init__(file_str)
        
    def get_type(self):
        '''
        Gets the file type (e.g., user, item or context) to parsers properties.
        :return: The file type.
        '''
        file_type = None
        try:
            file_type = self.file_parser.get(section='global', option='type')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return file_type 

    def get_number_attributes(self):
        '''
        Gets the number of attributes.
        :return: The number of attributes.
        '''
        number_attributes = None
        try:
            number_attributes = self.file_parser.getint(section='global', option='number_attributes')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        
        return number_attributes 
    
    def get_attribute_name_list(self):
        # sourcery skip: for-append-to-extend, use-fstring-for-concatenation
        '''
        Gets a list with the attribute names.
        :return: A list with the attribute names.
        '''
        attribute_name_list = []
        try:
            if number_attributes := self.get_number_attributes():
                for pos in range(1, number_attributes+1):
                    attribute_name_list.append(self.file_parser.get(section='attribute'+str(pos), option='name_attribute_'+str(pos)))
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return attribute_name_list

    def get_attribute_name_from_pos(self, position):
        '''
        Gets the name of an attribute from a specified position.
        :param position: The position of an attribute.
        :return: The name of an attribute.
        '''
        attribute_name = None
        try:        
            attribute_name = self.file_parser.get(section=f'attribute{str(position)}', option=f'name_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return attribute_name
    
    def get_position_from_attribute_name(self, attribute_name):
        # sourcery skip: inline-immediately-returned-variable, use-next
        '''
        Gets the position in the attribute name list given an attribute name.
        :param attribute_name: The attribute name.
        :return: The position in the list given an attribute name.
        '''
        attribute_name_list = self.get_attribute_name_list()
        position = None
        for i in range(len(attribute_name_list)):
            if str(attribute_name_list[i]) == str(attribute_name):
                position = i + 1
                break
        return position
        
    def get_type_attribute_from_pos(self, position):
        '''
        Gets the data type of an attribute.
        :param position: The position of an attribute.        
        :return: The data type of an attribute.
        '''
        type_attribute = None
        try:
            type_attribute = self.file_parser.get(section=f'attribute{str(position)}', option=f'type_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return type_attribute
    
    def get_generator_type_attribute_from_pos(self, position):
        '''
        Gets the name of the generator given the position of an attribute.
        :param position: The position of an attribute.
        :return: The name of the generator given the position of an attribute.
        '''
        generator_type_attribute = None
        try:        
            generator_type_attribute = self.file_parser.get(section=f'attribute{str(position)}', option=f'generator_type_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return generator_type_attribute

    def get_number_posible_values_attribute_from_pos(self, position):
        '''
        Gets the maximum number of values of an attribute.
        :param position: The position of an attribute.
        :return: The maximum number of values of an attribute.
        '''
        number_posible_values_attribute = None
        try:        
            number_posible_values_attribute = self.file_parser.getint(section=f'attribute{str(position)}', option=f'number_posible_values_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return number_posible_values_attribute

    def get_possible_values_attribute_list_from_pos(self, position):        
        # sourcery skip: for-append-to-extend
        '''
        Gets a list of possible values of an attribute, by using the attribute position.
        :param position: The position of an attribute.
        :return: A list of possible values of an attribute.
        '''
        possible_values_attribute_list = []
        number_posible_values_attribute = self.get_number_posible_values_attribute_from_pos(position=position)
        try:        
            if number_posible_values_attribute:
                for number in range(1, number_posible_values_attribute+1):
                    possible_values_attribute_list.append(self.file_parser.get(section=f'attribute{str(position)}', option=f'posible_value_{str(number)}_attribute_{str(position)}'))
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return possible_values_attribute_list
    
    def get_possible_values_attribute_list_from_name(self, attribute_name):
        '''
        Gets a list of possible values of an attribute, by using the attribute name.
        :param name: The name of an attribute.
        :return: A list of possible values of an attribute.
        '''
        possible_values_attribute_list = []
        try:
            if attribute_name != 'other':
                attribute_position = self.get_position_from_attribute_name(attribute_name)
                attribute_type = self.get_type_attribute_from_pos(position=attribute_position)
                if attribute_type == 'String': #or attribute_type == 'List':
                    possible_values_attribute_list = self.get_possible_values_attribute_list_from_pos(position=attribute_position)
                elif attribute_type == 'Boolean':
                    possible_values_attribute_list = [False, True]
                elif attribute_type == 'Integer':
                    minimum_value = self.get_minimum_value_attribute_from_pos(position=attribute_position)
                    maximum_value = self.get_maximum_value_attribute_from_pos(position=attribute_position)
                    possible_values_attribute_list = list(range(int(minimum_value), int(maximum_value)+1))
                elif attribute_type == 'Float':
                    minimum_value = self.get_minimum_value_attribute_from_pos(position=attribute_position)
                    maximum_value = self.get_maximum_value_attribute_from_pos(position=attribute_position)
                    possible_values_attribute_list_aux = np.arange(float(minimum_value), float(maximum_value)+0.1, 0.1).tolist()
                    possible_values_attribute_list = np.round(possible_values_attribute_list_aux, 2).tolist()
                elif attribute_type == 'List':
                    possible_values_attribute_list = self.get_component_attribute_list_from_pos(position=attribute_position)                  
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return possible_values_attribute_list    
    
    def get_input_parameter_attribute_from_pos(self, position):
        '''
        Gets the input parameter given the position of an attribute.
        :param position: The position of an attribute.
        :return: The input parameter given the position of an attribute.
        '''
        input_parameter_attribute = None
        try:
            input_parameter_attribute = self.file_parser.get(section=f'attribute{str(position)}', option=f'input_parameter_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            # logging.error(e)
            pass
        return input_parameter_attribute
    
    def get_input_parameter_subattribute_from_pos(self, position_attribute, position_subattribute):
        '''
        Gets the input parameter given the position of a subattribute.
        :param position_attribute: The position of an attribute.
        :param position_subattribute: The position of a subattribute.
        :return: The input parameter given the position of a subattribute.
        '''
        try:
            input_parameter_attribute = self.file_parser.get(section=f'attribute{str(position_attribute)}', option=f'input_parameter_subattribute_{str(position_subattribute)}_attribute_{str(position_attribute)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return input_parameter_attribute
        
    def get_subattribute_input_parameters_dict_from_pos(self, position_attribute):
        '''
        Gets a dictionary of input parameters for subattributes given the position of an attribute.

        :param position_attribute: The position of an attribute.
        :return: A dictionary with subattribute names as keys and input parameters as values.
        '''
        input_parameters_dict = {}
        number_maximum_subattributes = self.get_number_maximum_subattribute_from_pos(position_attribute)

        for position_subattribute in range(1, number_maximum_subattributes + 1):
            subattribute_name = self.get_name_subattribute_from_pos(position_attribute, position_subattribute)
            input_parameter = self.get_input_parameter_subattribute_from_pos(position_attribute, position_subattribute)

            # Check if the input_parameter is a string representation of a list
            if input_parameter and input_parameter.startswith('[') and input_parameter.endswith(']'):
                input_parameter = eval(input_parameter)

            input_parameters_dict[subattribute_name] = input_parameter

        return input_parameters_dict
    
    def get_subattribute_input_parameters_dict_from_name_attribute(self, name_attribute):
        """
        Gets a list of dictionaries with input parameters based on the attribute name.
        :param name_attribute: The name of the attribute.
        :return: A list of dictionaries with input parameters.
        """
        input_parameters_list = []
        number_attributes = self.get_number_attributes()
        position_attribute = None

        for pos in range(1, number_attributes + 1):
            if self.get_attribute_name_from_pos(pos) == name_attribute:
                position_attribute = pos
                break

        if position_attribute:
            input_parameters_string = self.file_parser.get(section=f"attribute{str(position_attribute)}", option=f"input_parameter_attribute_{str(position_attribute)}")
            
            if input_parameters_string:
                input_parameters_list = eval(input_parameters_string)

        return input_parameters_list

    def get_minimum_value_attribute_from_pos(self, position):
        '''
        Gets the minimum value of an attribute.
        :param position: The position of an attribute.        
        :return: The minimum value (like a number float) of an attribute.
        '''
        minimum_value_attribute = None
        try:        
            minimum_value_attribute = self.file_parser.get(section=f'attribute{str(position)}', option=f'minimum_value_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return minimum_value_attribute
    
    def get_maximum_value_attribute_from_pos(self, position):
        '''
        Gets the maximum value of an attribute.
        :param position: The position of an attribute.        
        :return: The maximum value (like a number float) of an attribute.
        '''
        maximum_value_attribute = None
        try:        
            maximum_value_attribute = self.file_parser.get(section=f'attribute{str(position)}', option=f'maximum_value_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return maximum_value_attribute
    
    def get_number_maximum_component_attribute_from_pos(self, position):
        '''
        Gets the number maximum of components of an attribute.
        :param position: The position of an attribute.        
        :return: The number maximum of components of an attribute.
        '''
        number_maximum_component_attribute = None
        try:
            number_maximum_component_attribute = self.file_parser.getint(section=f'attribute{str(position)}', option=f'number_maximum_component_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return number_maximum_component_attribute

    def get_type_component_attribute_from_pos(self, position):
        '''
        Gets the data type of an attribute component.
        :param position: The position of an attribute.        
        :return: The data type of an attribute component.
        '''
        type_component_attribute = None
        try:
            type_component_attribute = self.file_parser.get(section=f'attribute{str(position)}', option=f'type_component_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return type_component_attribute

    def get_component_attribute_list_from_pos(self, position):
        # sourcery skip: for-append-to-extend
        '''
        Gets a list with the components of an attribute.
        :param position: The position of an attribute.        
        :return: A list with the components of an attribute.
        '''
        component_attribute_list = []
        number_maximum_component_attribute = self.get_number_maximum_component_attribute_from_pos(position=position)
        try:
            if number_maximum_component_attribute:
                for number in range(1, number_maximum_component_attribute+1):
                    component_attribute_list.append(self.file_parser.get(section=f'attribute{str(position)}', option=f'component_{str(number)}_attribute_{str(position)}'))
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return component_attribute_list
        
    def get_number_maximum_subattribute_from_pos(self, position):
        '''
        Gets the number maximum of sub-attributes of an attribute.
        :param position: The position of an attribute.        
        :return: The number maximum of sub-attributes of an attribute.
        '''
        number_maximum_subattribute = None
        try:
            number_maximum_subattribute = self.file_parser.getint(section=f'attribute{str(position)}', option=f'number_maximum_subattribute_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return number_maximum_subattribute

    def get_name_subattribute_list_from_pos(self, position):
        # sourcery skip: for-append-to-extend
        '''
        Gets a list with the sub-attribute names of an attribute.
        :param position: The position of an attribute.        
        :return: A list with the sub-attribute names of an attribute.
        '''
        name_subattribute = []
        number_maximum_subattribute = self.get_number_maximum_subattribute_from_pos(position=position)
        try:
            if number_maximum_subattribute:
                for number in range(1, number_maximum_subattribute+1):
                    name_subattribute.append(self.file_parser.get(section=f'attribute{str(position)}', option=f'name_subattribute_{str(number)}_attribute_{str(position)}'))
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return name_subattribute

    def get_name_subattribute_from_pos(self, position_attribute, position_subattribute):
        '''
        Gets the name of a specific sub-attribute.
        :param position_attribute: The position of an attribute.    
        :param position_subattribute: The position of a sub-attribute.
        :return: The name of a specific sub-attribute.
        '''
        name_subattribute = None
        try:
            name_subattribute = self.file_parser.get(section=f'attribute{str(position_attribute)}', option=f'name_subattribute_{str(position_subattribute)}_attribute_{str(position_attribute)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return name_subattribute  
    
    def get_type_subattribute_from_pos(self, position_attribute, position_subattribute):
        '''
        Gets the data type of a specific sub-attribute.
        :param position_attribute: The position of an attribute.    
        :param position_subattribute: The position of a sub-attribute.
        :return: The data type of a specific sub-attribute.
        '''
        type_subattribute = None
        try:
            type_subattribute = self.file_parser.get(section=f'attribute{str(position_attribute)}', option=f'type_subattribute_{str(position_subattribute)}_attribute_{str(position_attribute)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return type_subattribute

    def get_important_profile_attribute_from_pos(self, position):
        '''
        Gets a boolean value that indicates if the attribute is important or not.
        :param position: The position of an attribute.        
        :return: True if the attribute is important and false otherwise.
        '''
        important_profile_attribute = None
        try:
            important_profile_attribute = self.file_parser.getboolean(section=f'attribute{str(position)}', option=f'important_profile_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return important_profile_attribute

    def get_ranking_order_by_attribute_from_pos(self, position):
        # sourcery skip: remove-unreachable-code
        '''
        Gets the order (ascending or descending) of importance of an attribute.
        :param position: The position of an attribute.        
        :return: The order (ascending or descending) of importance of an attribute.
        '''
        ranking_order_by_attribute = None
        try:
            ranking_order_by_attribute = self.file_parser.get(section=f'attribute{str(position)}', option=f'ranking_order_by_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return ranking_order_by_attribute        

    def get_number_important_weight_attribute(self):
        '''
        Gets the number of weights of an important attribute.        
        :return: The number of weights of an important attribute.
        '''
        number_important_weight_attribute = 0
        number_attributes = self.get_number_attributes()
        try:
            if number_attributes:                
                for position in range(1, number_attributes+1):
                    important_weight_attribute = self.get_important_weight_attribute_from_pos(position)
                    if important_weight_attribute:
                        number_important_weight_attribute += 1                    
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return number_important_weight_attribute
    
    def get_important_weight_attribute_from_pos(self, position):
        '''
        Gets the weight of an important attribute.
        :param position: The position of an attribute.        
        :return: The weight of an important attribute.
        '''
        important_weight_attribute = None
        try:
            important_weight_attribute = self.file_parser.getboolean(section=f'attribute{str(position)}', option=f'important_weight_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return important_weight_attribute
    
    def get_important_attribute_name_list(self):  # sourcery skip: for-append-to-extend
        '''
        Gets a attribute name list with important weight=True.        
        :return: A list of attribute names (relevant to the user).
        '''
        important_attribute_name_list = []
        number_attributes = self.get_number_attributes()
        try:
            if number_attributes:         
                for position in range(1, number_attributes+1):                    
                    if self.get_important_weight_attribute_from_pos(position):
                        important_attribute_name_list.append(str(self.get_attribute_name_from_pos(position)))
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return important_attribute_name_list
    
    def get_unique_value_attribute_from_pos(self, position):
        '''
        Gets True if the attribute to be generated will have a unique value and False if the attribute to be generated will have a random value.
        :param position: The position of an attribute.        
        :return: Boolean value indicating if the attribute to be generated will have a unique or random value.
        '''
        unique_value_attribute = None
        try:
            unique_value_attribute = self.file_parser.getboolean(section=f'attribute{str(position)}', option=f'unique_value_attribute_{str(position)}')
        except (NoOptionError, NoSectionError) as e:
            logging.error(e)
        return unique_value_attribute
