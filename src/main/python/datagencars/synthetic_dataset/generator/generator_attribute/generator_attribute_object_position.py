import random, ast
from datagencars.synthetic_dataset.generator.generator_attribute.generator_attribute import GeneratorAttribute

class GeneratorAttributeObjectPosition(GeneratorAttribute):
    '''
    A generator of attribute values representing 3D coordinates (latitude, longitude, and altitude) of a location. 
    @author Marcos Caballero Yus
    '''

    def __init__(self, schema_access):
        super().__init__(schema_access)

    def generate_attribute_value(self, position):
        # sourcery skip: extract-method, for-append-to-extend
        '''
        Generates an attribute value (address) of a instance.

        Example of item_schema.conf:
            [attribute8]
            name_attribute_8=object_position
            type_attribute_8=AttributeComposite
            number_maximum_subattribute_attribute_8=3
            name_subattribute_1_attribute_8=longitude
            name_subattribute_2_attribute_8=lattitude
            name_subattribute_3_attribute_8=altitude
            type_subattribute_1_attribute_8=float
            type_subattribute_2_attribute_8=float
            type_subattribute_3_attribute_8=float
            generator_type_attribute_8=ObjectPositionAttributeGenerator
        :param position: The position of an attribute.
        :return: The attribute value (location).
        '''
        attribute_name = self.schema_access.get_attribute_name_from_pos(position)       
        if attribute_name == 'user_profile_id':
            print('TODO')
        else:
            habitaciones = ast.literal_eval(self.schema_access.get_input_parameter_attribute_from_pos(position))
            habitacion = random.choice(habitaciones)  # Select a random dictionary from the list
            x = random.uniform(habitacion['x_min'], habitacion['x_max'])
            y = random.uniform(habitacion['y_min'], habitacion['y_max'])
            z = random.uniform(habitacion['z_min'], habitacion['z_max'])
            attribute_value = [x, y, z, habitacion['id']]
        return attribute_name, attribute_value