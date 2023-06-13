from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_address import GeneratorAttributeAddress
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_boolean_list import GeneratorAttributeBooleanList
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_correlation import GeneratorAttributeCorrelation
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_date import GeneratorAttributeDate
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_device import GeneratorDevice
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_fixed import GeneratorAttributeFixed
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_gaussian import GeneratorAttributeGaussian
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_object_position import GeneratorAttributeObjectPosition
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_random import GeneratorAttributeRandom
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute_url import GeneratorAttributeURL

import pandas as pd


class GeneratorInstance():

    def __init__(self, schema_access, generation_access=None, item_profile_access=None):        
        self.generation_access = generation_access
        self.schema_access = schema_access
        self.item_profile_access = item_profile_access        
    
    def generate_instance(self, instance=None, position_item_profile=None, with_noise=None):
        number_attributes = self.schema_access.get_number_attributes()
        attribute_list = []
        for position in range(1, number_attributes+1):
            generator_type = self.schema_access.get_generator_type_attribute_from_pos(position)
            if instance is None or pd.isna(instance[position]): 
                attribute_generator = None
                attribute_value = None
                if generator_type == 'CorrelationAttributeGenerator':
                    attribute_generator = GeneratorAttributeCorrelation(schema_access=self.schema_access, item_profile_access=self.item_profile_access, generation_access=self.generation_access)
                    _,attribute_value = attribute_generator.generate_attribute_value(position_attribute=position, position_item_profile=position_item_profile, with_noise=with_noise)
                else:                 
                    if generator_type == 'RandomAttributeGenerator':
                        attribute_generator = GeneratorAttributeRandom(self.schema_access)
                    elif generator_type == 'GaussianAttributeGenerator':
                        attribute_generator = GeneratorAttributeGaussian(self.schema_access)
                    elif generator_type == 'FixedAttributeGenerator':
                        attribute_generator = GeneratorAttributeFixed(self.schema_access)
                    elif generator_type == 'URLAttributeGenerator':
                        attribute_generator = GeneratorAttributeURL(self.schema_access)                
                    elif generator_type == 'AddressAttributeGenerator':
                        attribute_generator = GeneratorAttributeAddress(self.schema_access)          
                    elif generator_type == 'DateAttributeGenerator':
                        attribute_generator = GeneratorAttributeDate(self.schema_access)
                    elif generator_type == 'BooleanListAttributeGenerator':
                        attribute_generator = GeneratorAttributeBooleanList(self.schema_access)
                    elif generator_type == 'ObjectPositionAttributeGenerator':
                        attribute_generator = GeneratorAttributeObjectPosition(self.schema_access)
                    elif generator_type == 'DeviceGenerator':
                        attribute_generator = GeneratorDevice(self.schema_access)
                    _, attribute_value = attribute_generator.generate_attribute_value(position)
            else:
                attribute_value = instance[position]
            attribute_list.append(attribute_value)
        return attribute_list
