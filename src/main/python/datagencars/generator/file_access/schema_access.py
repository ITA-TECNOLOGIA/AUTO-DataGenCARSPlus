import logging
from configparser import NoOptionError, NoSectionError

from datagencars.generator.file_access.data_access import DataAccess


class SchemaAccess(DataAccess):
    '''
    Gets the values of the properties stored in a schema file (user_schema.txt, item_schema.txt or context_schema.txt). 
    @author Maria del Carmen Rodriguez-Hernandez 
    '''

    def __init__(self, file_path):
        super().__init__(file_path)
        
    # def get_type(self):
    #     '''
    #     Gets the file type (e.g., user, item or context) to parsers properties.
    #     :return: The file type.
    #     '''
    #     file_type = None
    #     try:
    #         file_type = self.file_parser.get(section='global', option='type')
    #     except (NoOptionError, NoSectionError) as e:            
    #         logging.error(e)
    #     return file_type 

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

    # def get_number_import(self):
    #     '''
    #     Gets the number of required imports.
    #     :return: The number of imports.
    #     '''
    #     number_import = None
    #     try:    
    #         number_import = self.file_parser.getint(section='global', option='number_import')
    #     except (NoOptionError, NoSectionError) as e:            
    #         logging.error(e)
    #     return number_import

    # def get_input_import_list(self):        
    #     # sourcery skip: for-append-to-extend, use-fstring-for-concatenation
    #     '''
    #     Gets a list with the required input imports.
    #     :return: A list with the input imports.
    #     '''
    #     input_import_list = []
    #     try:
    #         if number_import := self.get_number_import():
    #             for pos in range(1, number_import+1):
    #                 input_import_list.append(self.file_parser.get(section='global', option='input_import_'+str(pos)))
    #     except (NoOptionError, NoSectionError) as e:            
    #         logging.error(e)
    #     return input_import_list

    # def get_input_import_from_pos(self, position):
    #     '''
    #     Gets an input import from a specified position.
    #     :param position: The position of an input import.
    #     :return: An input import.
    #     '''
    #     input_import = None
    #     try:        
    #         input_import = self.file_parser.get(section='global', option=f'input_import_{str(position)}')
    #     except (NoOptionError, NoSectionError) as e:            
    #         logging.error(e)
    #     return input_import

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

    # def get_position_from_attribute_name(self, attribute_name):
    #     # sourcery skip: inline-immediately-returned-variable, use-next
    #     '''
    #     Gets the position in the attribute name list given an attribute name.
    #     :param attribute_name: The attribute name.
    #     :return: The position in the list given an attribute name.
    #     '''
    #     attribute_name_list = self.get_attribute_name_list()
    #     position = None
    #     for i in range(len(attribute_name_list)):
    #         if str(attribute_name_list[i]) == str(attribute_name):
    #             position = i + 1
    #             break
    #     return position
        
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
            logging.error(e)
        return input_parameter_attribute

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
        Gets a list of possible values of an attribute.
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
    
    # def get_number_posible_values_subattribute_from_pos(self, position_attribute, position_subattribute):
    #     '''
    #     Gets the maximum number of values by sub-attribute.
    #     :param position_attribute: The position of an attribute.
    #     :param position_subattribute: The position of an sub-attribute.
    #     :return: The maximum number of values by sub-attribute.
    #     '''
    #     number_posible_values_subattribute = None
    #     try:        
    #         number_posible_values_subattribute = self.file_parser.getint(section=f'attribute{str(position)}', option=f'number_posible_values_subattribute_{str(position_subattribute)}_attribute_{str(position_attribute)}')
    #     except (NoOptionError, NoSectionError) as e:            
    #         logging.error(e)
    #     return number_posible_values_subattribute
    
    # def get_posible_value_subattribute_list_from_pos(self, position_attribute, position_subattribute):
    #     # sourcery skip: for-append-to-extend
    #     '''
    #     Gets a list of possible values of an sub-attribute.
    #     :param position_attribute: The position of an attribute.
    #     :param position_subattribute: The position of an sub-attribute.
    #     :return: A list of possible values of an sub-attribute.
    #     '''
    #     posible_value_subattribute_list = []
    #     number_posible_values_subattribute = self.get_number_posible_values_subattribute_from_pos(position_attribute, position_subattribute)
    #     try:
    #         if number_posible_values_subattribute:
    #             for number in range(1, number_posible_values_subattribute+1):
    #                 posible_value_subattribute_list.append(self.file_parser.get(section=f'attribute{str(position)}', option=f'posible_value_{str(number)}_subattribute_{str(position_subattribute)}_attribute_{str(position_attribute)}'))
    #     except (NoOptionError, NoSectionError) as e:            
    #         logging.error(e)
    #     return posible_value_subattribute_list
    
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
    
    # def get_type_component_attribute_from_pos(self, position):
    #     '''
    #     Gets the data type of an attribute component.
    #     :param position: The position of an attribute.        
    #     :return: The data type of an attribute component.
    #     '''
    #     type_component_attribute = None
    #     try:
    #         type_component_attribute = self.file_parser.get(section=f'attribute{str(position)}', option=f'type_component_attribute_{str(position)}')
    #     except (NoOptionError, NoSectionError) as e:
    #         logging.error(e)
    #     return type_component_attribute
    
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

    def get_component_attribute_list_from_pos(self, position):
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

    # def get_name_subattribute_from_pos(self, position_attribute, position_subattribute):
    #     '''
    #     Gets the name of a specific sub-attribute.
    #     :param position_attribute: The position of an attribute.    
    #     :param position_subattribute: The position of a sub-attribute.
    #     :return: The name of a specific sub-attribute.
    #     '''
    #     name_subattribute = None
    #     try:
    #         name_subattribute = self.file_parser.get(section=f'attribute{str(position_attribute)}', option=f'name_subattribute_{str(position_subattribute)}_attribute_{str(position_attribute)}')
    #     except (NoOptionError, NoSectionError) as e:
    #         logging.error(e)
    #     return name_subattribute
    
    # def get_type_subattribute_from_pos(self, position_attribute, position_subattribute):
    #     '''
    #     Gets the data type of a specific sub-attribute.
    #     :param position_attribute: The position of an attribute.    
    #     :param position_subattribute: The position of a sub-attribute.
    #     :return: The data type of a specific sub-attribute.
    #     '''
    #     type_subattribute = None
    #     try:
    #         type_subattribute = self.file_parser.get(section=f'attribute{str(position_attribute)}', option=f'type_subattribute_{str(position_subattribute)}_attribute_{str(position_attribute)}')
    #     except (NoOptionError, NoSectionError) as e:
    #         logging.error(e)
    #     return type_subattribute

    # def get_important_profile_attribute_from_pos(self, position):
    #     '''
    #     Gets a boolean value that indicates if the attribute is important or not.
    #     :param position: The position of an attribute.        
    #     :return: True if the attribute is important and false otherwise.
    #     '''
    #     important_profile_attribute = None
    #     try:
    #         important_profile_attribute = self.file_parser.getboolean(section=f'attribute{str(position)}', option=f'important_profile_attribute_{str(position)}')
    #     except (NoOptionError, NoSectionError) as e:
    #         logging.error(e)
    #     return important_profile_attribute
    
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
    
    # def get_important_weight_attribute_from_pos(self, position):
    #     '''
    #     Gets the weight of an important attribute.
    #     :param position: The position of an attribute.        
    #     :return: The weight of an important attribute.
    #     '''
    #     important_weight_attribute = None
    #     try:
    #         important_weight_attribute = self.file_parser.getboolean(section=f'attribute{str(position)}', option=f'important_weight_attribute_{str(position)}')
    #     except (NoOptionError, NoSectionError) as e:
    #         logging.error(e)
    #     return important_weight_attribute

    # def get_number_important_weight_attribute(self):
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


# TODO:
# public double getPossibleValuesPercentageAttribute(int position, int possibleValuePosition)
# public double getAverageValueAttribute(int position)  
# public double getStandardDeviationValueAttribute(int position)
# public boolean getFixedBoundariesAttribute(int position)
# public Boolean getUniqueValueAttribute(int position)
# public String getDistribution(int position)
# public Map<String, List<String>> getValueFor(String nameAttribute)

    
# schema_access = SchemaAccess(file_path='resources/data/user_scheme.conf')
# # schema_access = SchemaAccess(file_path='resources/data/item_scheme.conf')
# # schema_access = SchemaAccess(file_path='resources/data/context_scheme.conf')

# item_type = schema_access.get_type()
# print(item_type)
# number_attributes = schema_access.get_number_attributes()
# print(number_attributes)
# number_import = schema_access.get_number_import()
# print(number_import)
# input_import_list = schema_access.get_input_import_list()
# print(input_import_list)
# input_import=schema_access.get_input_import_from_pos(position=1)
# print(input_import)
# attribute_name_list=schema_access.get_attribute_name_list()
# print(attribute_name_list)
# attribute_name = schema_access.get_attribute_name_from_pos(position=1)
# print(attribute_name)
# position = schema_access.get_position_from_attribute_name(attribute_name='gender')
# print(position)
# input_parameter_attribute = schema_access.get_input_parameter_attribute_from_pos(position=1)
# print(input_parameter_attribute)
# generator_type_attribute = schema_access.get_generator_type_attribute_from_pos(position=1)
# print(generator_type_attribute)
# number_posible_values_attribute = schema_access.get_number_posible_values_attribute_from_pos(position=2)
# print(number_posible_values_attribute)
# possible_values_attribute_list = schema_access.get_possible_values_attribute_list_from_pos(position=3)
# print(possible_values_attribute_list)
# number_posible_values_subattribute = schema_access.get_number_posible_values_subattribute_from_pos(position_attribute=6, position_subattribute=2)
# print(number_posible_values_subattribute)
# posible_value_subattribute_list = schema_access.get_posible_value_subattribute_list_from_pos(position_attribute=6, position_subattribute=2)
# print(posible_value_subattribute_list)
# minimum_value_attribute = schema_access.get_minimum_value_attribute_from_pos(position=1)
# print(minimum_value_attribute)
# maximum_value_attribute = schema_access.get_maximum_value_attribute_from_pos(position=1)
# print(maximum_value_attribute)
# type_attribute = schema_access.get_type_attribute_from_pos(position=1)
# print(type_attribute)
# type_component_attribute = schema_access.get_type_component_attribute_from_pos(position=6)
# print(type_component_attribute)
# number_maximum_component_attribute = schema_access.get_number_maximum_component_attribute_from_pos(position=6)
# print(number_maximum_component_attribute)
# component_attribute = schema_access.get_component_attribute_from_pos(position=6)
# print(component_attribute)
# number_maximum_subattribute = schema_access.get_number_maximum_subattribute_from_pos(position=1)
# print(number_maximum_subattribute)
# name_subattribute_list = schema_access.get_name_subattribute_list_from_pos(position=1)
# print(name_subattribute_list)
# name_subattribute = schema_access.get_name_subattribute_from_pos(position_attribute=1, position_subattribute=1)
# print(name_subattribute)
# type_subattribute = schema_access.get_type_subattribute_from_pos(position_attribute=1, position_subattribute=1)
# print(type_subattribute)
# important_profile_attribute = schema_access.get_important_profile_attribute_from_pos(position=16)
# print(important_profile_attribute)
# ranking_order_by_attribute = schema_access.get_ranking_order_by_attribute_from_pos(position=15)
# print(ranking_order_by_attribute)
# important_weight_attribute = schema_access.get_important_weight_attribute_from_pos(position=15)
# print(important_weight_attribute)
# number_important_weight_attribute = schema_access.get_number_important_weight_attribute()
# print(number_important_weight_attribute)
