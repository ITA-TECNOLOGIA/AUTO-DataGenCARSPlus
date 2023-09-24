import logging
import unittest

import pandas as pd
from datagencars.existing_dataset.replace_null_values.replace_null_values import ReplaceNullValues
from streamlit_app.preprocess_dataset import wf_replace_null_values


class TestGeneratorSyntheticDataset(unittest.TestCase):

    def setUp(self):        
        # item_df:
        item_file_path = 'resources/existing_dataset/context/preferencial_rating/sts/item.csv'
        self.item_df = pd.read_csv(item_file_path, encoding='utf-8', index_col=False, sep=';')
        # context_df:
        context_file_path = 'resources/existing_dataset/context/preferencial_rating/sts/context.csv'
        self.context_df = pd.read_csv(context_file_path, encoding='utf-8', index_col=False, sep=';')
                
        # Constructor:
        self.__replace_nulls_item = ReplaceNullValues(file_df=self.item_df)
        self.__replace_nulls_context = ReplaceNullValues(file_df=self.context_df)
     
    def tearDown(self):
        del self.__replace_nulls_item
        del self.__replace_nulls_context

    def test_infer_data_type_url(self):
        '''
        Infering data type: URL (composite).
        '''
        attribute_value_list = ['http://www.umami_burger.com']
        generator_type, attribute_type, __, type_subattribute = wf_replace_null_values.infer_data_type(attribute_value_list)
        logging.info(f'generator_type: {generator_type}')
        logging.info(f'attribute_type: {attribute_type}')    
        logging.info(f'type_subattribute: {type_subattribute}')    
        self.assertEqual(generator_type, 'URLAttributeGenerator')
        self.assertEqual(attribute_type, 'AttributeComposite')        
        self.assertEqual(type_subattribute, 'String')   

    def test_infer_data_type_address(self):
        '''
        Infering data type: Address (composite).
        '''
        attribute_value_list = ["['Piazza Dogana - Zollstangenplatz', '3', '39100', '11.354651', '11.374649']", "['Via Museo - Museumstraße', '19', '39100', '11.34651', '11.364649']", "['Via Cavour - Cavourstraße', '8', '39100', '11.354651', '11.37465']", "['Via Portici - Laubengasse', '51', '39100', '11.344651', '11.364649']", "['Via dei Conciapelli - Gerbergasse', '25', '39100', '11.354651', '11.374649']", "['Via Andreas Hofer - Andreas-Hofer-Straße', '30', '39100', '11.354651', '11.374649']", "['Via Andreas Hofer - Andreas-Hofer-Straße', '8', '39100', '11.354651', '11.374649']", "['Viale Druso - Drususallee', '50', '39100', '11.33465', '11.354649']", "['Piazza delle Erbe - Obstmarkt', '17', '39100', '11.344651', '11.364649']", "['Via Cassa di Risparmio - Sparkassenstraße', '12', '39100', '11.344651', '11.364649']", "['Via Alto Adige - Südtiroler Straße', '60', '39100', '11.35465', '11.364649']"]
        generator_type, attribute_type, __, type_subattribute = wf_replace_null_values.infer_data_type(attribute_value_list)
        logging.info(f'generator_type: {generator_type}')
        logging.info(f'attribute_type: {attribute_type}')    
        logging.info(f'type_subattribute: {type_subattribute}')
        self.assertEqual(generator_type, 'AddressAttributeGenerator')
        self.assertEqual(attribute_type, 'AttributeComposite')    
        self.assertEqual(type_subattribute, 'String')   

    def test_infer_data_type_fixed_str(self):
        '''
        Infering data type: Fixed (str).
        '''
        attribute_value_list = ['California']
        generator_type, attribute_type, __, __ = wf_replace_null_values.infer_data_type(attribute_value_list)
        logging.info(f'generator_type: {generator_type}')
        logging.info(f'attribute_type: {attribute_type}')
        self.assertEqual(generator_type, 'FixedAttributeGenerator')
        self.assertEqual(attribute_type, 'String')    
    
    def test_infer_data_type_fixed_int(self):
        '''
        Infering data type: Fixed (int).
        '''
        attribute_value_list = [50004]
        generator_type, attribute_type, __, __ = wf_replace_null_values.infer_data_type(attribute_value_list)
        logging.info(f'generator_type: {generator_type}')
        logging.info(f'attribute_type: {attribute_type}')
        self.assertEqual(generator_type, 'FixedAttributeGenerator')
        self.assertEqual(attribute_type, 'Integer')

    def test_infer_data_type_fixed_bool(self):
        '''
        Infering data type: Fixed (bool).
        '''
        attribute_value_list = [True]
        generator_type, attribute_type, __, __ = wf_replace_null_values.infer_data_type(attribute_value_list)
        logging.info(f'generator_type: {generator_type}')
        logging.info(f'attribute_type: {attribute_type}')
        self.assertEqual(generator_type, 'FixedAttributeGenerator')
        self.assertEqual(attribute_type, 'Boolean') 

    def test_infer_data_type_random_int(self):
        '''
        Infering data type: Numerical (int)--> Random (int).
        '''
        attribute_value_list = [976091136, 976197635, 976304133, 976490502, 976211977, 976599054, 976732176, 976271378, 976973843, 976035864, 976408607, 976115745, 976961569]    
        generator_type, attribute_type, __, __ = wf_replace_null_values.infer_data_type(attribute_value_list)
        logging.info(f'generator_type: {generator_type}')
        logging.info(f'attribute_type: {attribute_type}')    
        self.assertEqual(generator_type, 'RandomAttributeGenerator')
        self.assertEqual(attribute_type, 'Integer')

    def test_infer_data_type_random_float(self):
        '''
        Infering data type: Numerical (float)--> Random (float).
        '''
        attribute_value_list = [5.0, 4.0, 3.0, 2.0, 1.0]    
        generator_type, attribute_type, __, __ = wf_replace_null_values.infer_data_type(attribute_value_list)
        logging.info(f'generator_type: {generator_type}')
        logging.info(f'attribute_type: {attribute_type}')
        self.assertEqual(generator_type, 'RandomAttributeGenerator')
        self.assertEqual(attribute_type, 'Float')

    def test_infer_data_type_random_str(self):
        '''
        Infering data type: Categorical (str)--> Random (str).
        '''
        attribute_value_list = ['$$$$', '$', '$$', '$$$', 'free']
        generator_type, attribute_type, __, __ = wf_replace_null_values.infer_data_type(attribute_value_list)
        logging.info(f'generator_type: {generator_type}')
        logging.info(f'attribute_type: {attribute_type}')    
        self.assertEqual(generator_type, 'RandomAttributeGenerator')
        self.assertEqual(attribute_type, 'String')

    def test_infer_data_type_random_bool(self):
        '''
        Infering data type: Categorical (bool)--> Random (bool).
        '''
        attribute_value_list = [False, True]  
        generator_type, attribute_type, __, __ = wf_replace_null_values.infer_data_type(attribute_value_list)
        logging.info(f'generator_type: {generator_type}')
        logging.info(f'attribute_type: {attribute_type}')
        self.assertEqual(generator_type, 'RandomAttributeGenerator')
        self.assertEqual(attribute_type, 'Boolean')

    def test_infer_data_type_booleanlist(self):
        '''
        Infering data type: BooleanList.
        '''
        attribute_value_list = ["['monday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']", "['monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']", "['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'sunday']", "['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']", "['tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']", "['monday', 'tuesday', 'wednesday', 'thursday', 'saturday', 'sunday']", "['monday', 'tuesday', 'thursday', 'friday', 'saturday', 'sunday']"]
        generator_type, attribute_type, type_component, __ = wf_replace_null_values.infer_data_type(attribute_value_list)
        logging.info(f'generator_type: {generator_type}')
        logging.info(f'attribute_type: {attribute_type}')        
        logging.info(f'type_component: {type_component}') 
        self.assertEqual(generator_type, 'BooleanListAttributeGenerator')
        self.assertEqual(attribute_type, 'List')  
        self.assertEqual(type_component, 'Boolean')  

    def test_infer_data_type_date(self):
        '''
        Infering data type: Date.
        '''
        attribute_value_list = ['11-11-1975', '19-7-1961', '7-4-1967', '5-8-1964', '30-1-1976', '19-9-1983', '2-10-1981', '16-1-1992', '15-4-1993', '15-1-1957']
        generator_type, attribute_type, __, __ = wf_replace_null_values.infer_data_type(attribute_value_list)
        logging.info(f'generator_type: {generator_type}')
        logging.info(f'attribute_type: {attribute_type}')        
        self.assertEqual(generator_type, 'DateAttributeGenerator')
        self.assertEqual(attribute_type, 'String')        
    
    def test_replace_null_values_item(self):
        '''        
        Replacing null values in the schema file: "item.csv".
        '''       
        schema = wf_replace_null_values.infer_schema(df=self.item_df, file_type='item')
        new_df = self.__replace_nulls_item.regenerate_item_file(item_schema=schema)
        logging.info(f'new_item: {new_df}')
        self.assertEqual(new_df.isnull().any().any(), False)

    def test_replace_null_values_context(self):
        '''        
        Replacing null values in the schema file: "context.csv".
        '''        
        schema = wf_replace_null_values.infer_schema(df=self.context_df, file_type='context')
        new_df = self.__replace_nulls_context.regenerate_context_file(context_schema=schema)
        logging.info(f'new_item: {new_df}')
        self.assertEqual(new_df.isnull().any().any(), False)


if __name__ == '__main__':
    unittest.main()
