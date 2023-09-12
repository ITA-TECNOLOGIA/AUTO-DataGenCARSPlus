import random, ast
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute import GeneratorAttribute

class GeneratorAttributeDevice(GeneratorAttribute):
    '''
    A generator of attribute values representing a device
    (browserName, browserVersion, deviceName, deviceType, deviceVendor, osName, osVersion) 
 
    @author Marcos Caballero Yus
    '''

    def __init__(self, schema_access):
        super().__init__(schema_access)

    def generate_attribute_value(self, position):
        # sourcery skip: extract-method, for-append-to-extend
        '''
        Generates an attribute value (device) of a instance.

        Example of context_schema.conf:
            [attribute1]
            name_attribute_1=device_data
            type_attribute_1=List
            generator_type_attribute_1=DeviceGenerator
            number_maximum_subattribute_attribute_1=5
            name_subattribute_1_attribute_1=browserName
            name_subattribute_2_attribute_1=browserVersion
            name_subattribute_3_attribute_1=deviceType
            name_subattribute_4_attribute_1=osName
            name_subattribute_5_attribute_1=osVersion
            type_subattribute_1_attribute_1=String
            type_subattribute_2_attribute_1=String
            type_subattribute_3_attribute_1=String
            type_subattribute_4_attribute_1=String
            type_subattribute_5_attribute_1=String
            input_parameter_subattribute_1_attribute_1=["Chrome", "Safari", "Firefox", "Mobile Safari", "GSA", "Edge", "Samsung Browser", "Opera", "MIUI Browser"]
            input_parameter_subattribute_2_attribute_1=[]
            input_parameter_subattribute_3_attribute_1=[]
            input_parameter_subattribute_4_attribute_1=["Android", "Windows", "Mac OS", "iOS", "Linux", "Chromium OS"]
            input_parameter_subattribute_5_attribute_1=[]
        :param position: The position of an attribute.
        :return: The attribute value (device).
        '''
        attribute_name = self.schema_access.get_attribute_name_from_pos(position)       
        if attribute_name == 'user_profile_id':
            print('TODO')
        else:
            params = self.schema_access.get_subattribute_input_parameters_dict_from_pos(position)

            attribute_value = {
                "browserName": random.choice(params["browserName"]),
                "browserVersion": f"{random.randint(80, 110)}.{random.randint(0, 9999)}.{random.randint(0, 9999)}.{random.randint(0, 9999)}",
                "deviceType": random.choice([False, "undefined"]),
                "osName": random.choice(params["osName"]),
                "osVersion": f"{random.randint(7, 15)}.{random.randint(0, 7)}.{random.randint(0, 7)}"
            }
        return attribute_name, attribute_value
