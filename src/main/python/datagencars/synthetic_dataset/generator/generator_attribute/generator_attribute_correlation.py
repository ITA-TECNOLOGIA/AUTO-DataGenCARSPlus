import logging
import random

import numpy as np
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute import GeneratorAttribute


class GeneratorAttributeCorrelation(GeneratorAttribute):

    def __init__(self, schema_access, item_profile_access, generation_access):
        super().__init__(schema_access)
        self.item_profile_access = item_profile_access
        self.generation_access = generation_access

    def generate_attribute_value(self, position_attribute, position_item_profile, with_noise):
        # sourcery skip: extract-duplicate-method, extract-method, hoist-similar-statement-from-if, hoist-statement-from-if, inline-immediately-returned-variable, low-code-quality, merge-comparisons, merge-duplicate-blocks, merge-else-if-into-elif, move-assign-in-block, remove-redundant-if, remove-redundant-slice-index, split-or-ifs
        '''
        Generates an attribute value (random with correlation) of a instance.

        Example of item_schema.conf:
            [attribute16]
            name_attribute_16=quality_service
            type_attribute_16=String
            number_posible_values_attribute_16=5
            posible_value_1_attribute_16=excellent
            posible_value_2_attribute_16=good
            posible_value_3_attribute_16=normal
            posible_value_4_attribute_16=bad
            posible_value_5_attribute_16=dreadful
            generator_type_attribute_16=CorrelationAttributeGenerator
            important_profile_attribute_16=true
            ranking_order_by_attribute_16=desc
            important_weight_attribute_16=true
        :param position: The position of an attribute.
        :return: The attribute value (random with correlation). 
        '''
        attribute_value = None
        attribute_name = self.schema_access.get_attribute_name_from_pos(position_attribute)
        if attribute_name == 'id_user_profile':
            print('TODO')
        else:
            name_profile = self.item_profile_access.get_name_profile_from_pos(position_item_profile)
            type_attribute = self.schema_access.get_type_attribute_from_pos(position_attribute)
            if type_attribute in ['Integer', 'Float']:
                minimum_value = self.schema_access.get_minimum_value_attribute_from_pos(position_attribute)
                maximum_value = self.schema_access.get_maximum_value_attribute_from_pos(position_attribute)
                if type_attribute == 'Integer':
                    # Generating a list of int values. 
                    array_np = np.array(list(range(int(minimum_value), int(maximum_value)+1)))
                elif type_attribute == 'Float':
                    # Generating a list of float values with 0.1 increment.
                    array_np = np.arange(float(minimum_value), float(maximum_value)+0.1, 0.1)
                # Verifying the ranking order (asc or desc), reversing the order if necessary.
                ranking_order = self.schema_access.get_ranking_order_by_attribute_from_pos(position_attribute)
                possible_values_attribute_list = []
                if ranking_order == 'asc':
                    possible_values_attribute_list = sorted(array_np)
                elif ranking_order == 'desc':
                    possible_values_attribute_list = sorted(array_np, reverse=True)
                else:                   
                    raise Exception(f'The schema file has no ranking_order_by_attribute_{str(position_attribute)} property.')
                attribute_value = self.get_attribute_value_for_numeric_str(possible_values_attribute_list, ranking_order, with_noise, name_profile)                
            elif type_attribute == 'String':                
                possible_values_attribute_list = self.schema_access.get_possible_values_attribute_list_from_pos(position_attribute)
                ranking_order = self.schema_access.get_ranking_order_by_attribute_from_pos(position_attribute)
                attribute_value = self.get_attribute_value_for_numeric_str(possible_values_attribute_list, ranking_order, with_noise, name_profile)
            elif type_attribute == 'Boolean':                
                # Including noise:                
                if with_noise:
                   # Without noise:                
                    if name_profile == 'good':
                        attribute_value = False
                    elif name_profile == 'normal':
                        attribute_value = bool(random.choice([True, False]))
                    elif name_profile == 'bad':
                        attribute_value = True 
                else:
                    # Without noise:                
                    if name_profile == 'good':
                        attribute_value = True
                    elif name_profile == 'normal':
                        attribute_value = bool(random.choice([True, False]))
                    elif name_profile == 'bad':
                        attribute_value = False
        return attribute_name, attribute_value

    def get_attribute_value_for_numeric_str(self, possible_values_attribute_list, ranking_order, with_noise, name_profile):
        '''
        Get attribute value from a list of possible attribute values for data type integer, float and string, 
        by considering the ranking order, noise and name item profile.
        :param possible_values_attribute_list: A list with possible values of attribute (e.g., [1, 2, 3, 4, 5] or [excellent, good, normal, bad, dreadful]).
        :param ranking_order: The ranking order (asc --> [1, 2, 3, 4, 5], [excellent, good, normal, bad, dreadful] or desc --> [5, 4, 3, 2, 1], [dreadful, bad, normal, good, excellent])
        :param with_noise: True means that noise will be introduced during the generation of the attribute value and False in the other case.
        :param name_profile: The name of the current item profile (str value: 'good', 'normal' or 'bad').
        :return: The attribute value considering correlations from an item profile.
        '''
        # sourcery skip: hoist-similar-statement-from-if, hoist-statement-from-if, merge-else-if-into-elif, remove-redundant-slice-index, switch
        attribute_value = None
        # Determining the position of the middle of a list.
        low = 0
        high = len(possible_values_attribute_list) - 1
        pos_middle_value = int((low+high)/2)
        # Partitions the list by profile:
        overlap_midpoint_left = self.item_profile_access.get_overlap_midpoint_left_profile()
        overlap_midpoint_right = self.item_profile_access.get_overlap_midpoint_right_profile()
        possible_values_attribute_list_part1 = possible_values_attribute_list_part2 = possible_values_attribute_list_part3 = []
        if (overlap_midpoint_left != 0) and (overlap_midpoint_right != 0):                  
            # Manual partition: a[start:stop]  # items start through stop-1
            # First part: 
            possible_values_attribute_list_part1  = possible_values_attribute_list[0:pos_middle_value]
            # Second part:
            possible_values_attribute_list_part2  = possible_values_attribute_list[pos_middle_value-overlap_midpoint_left:pos_middle_value+overlap_midpoint_right+1]
            # Third part:
            possible_values_attribute_list_part3 =  possible_values_attribute_list[pos_middle_value+1:]
        else:
            # Partition by default: a[start:stop]  # items start through stop-1
            # First part:
            possible_values_attribute_list_part1  = possible_values_attribute_list[0:pos_middle_value]
            # Second part:
            possible_values_attribute_list_part2  = possible_values_attribute_list[pos_middle_value]
            # Third part:
            possible_values_attribute_list_part3 =  possible_values_attribute_list[pos_middle_value+1:]
        item_profile_dict = {}
        if ranking_order == 'asc':
            item_profile_dict['bad'] = possible_values_attribute_list_part1
            item_profile_dict['normal'] = possible_values_attribute_list_part2
            item_profile_dict['good'] = possible_values_attribute_list_part3
        elif ranking_order == 'desc':
            item_profile_dict['good'] = possible_values_attribute_list_part1
            item_profile_dict['normal'] = possible_values_attribute_list_part2
            item_profile_dict['bad'] = possible_values_attribute_list_part3
        # Including noise:                
        if with_noise:
            if name_profile == 'good':
                attribute_value = random.choice(item_profile_dict['bad'])             
            elif name_profile == 'normal':
                attribute_value = random.choice(item_profile_dict['good']+item_profile_dict['bad'])
            elif name_profile == 'bad':
                attribute_value = random.choice(item_profile_dict['good'])
        else:
            # Without noise:
            if name_profile == 'good':
                attribute_value = random.choice(item_profile_dict['good'])
            elif name_profile == 'normal':
                attribute_value = random.choice(item_profile_dict['normal'])
            elif name_profile == 'bad':
                attribute_value = random.choice(item_profile_dict['bad'])
        return attribute_value

# from datagencars.generator.file_access.schema_access import SchemaAccess
# item_schema_access = SchemaAccess(file_path='resources/data/item_schema.conf')
# item_profile_access = ItemProfileAccess(file_path='resources/data/item_profile.conf')
# generation_access = GenerationAccess(file_path='resources/data/generation_config.conf')
# correlation_attribute_generator = CorrelationAttributeGenerator(schema_access=item_schema_access, item_profile_access=item_profile_access, generation_access=generation_access)
# attribute_name, attribute_value = correlation_attribute_generator.generate_attribute_value(position_attribute=16, position_item_profile=3, with_noise=True) # position=18, position=16
# print('attribute_name: ', attribute_name)
# print('attribute_value: ', attribute_value)