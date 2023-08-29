import console
import pandas as pd
import streamlit as st
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_context import AccessContext
from datagencars.existing_dataset.replicate_dataset.access_dataset.access_item import AccessItem
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util
from streamlit_app.workflow_graph import workflow_image


def generate(with_context):
    """
    Generates the user profile.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """
    # WF --> Generate user profile:
    st.header('Workflow: Generate user profile')
    # Help information:
    help_information.help_user_profile_wf()
    # Worflow image:
    init_step = 'True'
    optional_value_list = [('NULLValues', str(True)), ('NULLValuesC', str(True)), ('NULLValuesI', str(True)), ('UPManual', 'True'), ('UPAutomatic', 'True')]
    workflow_image.show_wf(wf_name='GenerateUserProfile', init_step=init_step, with_context=True, optional_value_list=optional_value_list)
    st.markdown("""---""")
        
    # Choosing user profile generation options (manual or automatic):
    up_options = st.selectbox(label='Choose an option to generate the user profile:', options=config.UP_OPTIONS)

    # Automatic generation of the user profile:
    if up_options == 'Automatic':
        # Loading dataset:
        if with_context:
            user_df, item_df, context_df, rating_df = wf_util.load_dataset(file_type_list=config.DATASET_CARS, wf_type='wf_up')
        else:
            user_df, item_df, __, rating_df = wf_util.load_dataset(file_type_list=config.DATASET_RS, wf_type='wf_up')

    elif up_options == 'Manual':
        st.write('Manual')

    
    
   

    

    

    # # TAB --> Replace NULL values:
    # new_item_df = pd.DataFrame()
    # new_context_df = pd.DataFrame()        
    # with tab_replace_null_values:
    #     if up_option == 'Manual':
    #         upauto = False
    #         upmanual = True
    #     else:
    #         upauto = True
    #         upmanual = False
    #     if with_context:
    #         __, __, new_item_df, new_context_df = wf_util.tab_replace_null('GenerateUserProfile', with_context, item_df, context_df, [('UPAutomatic', str(upauto)), ('UPManual', str(upmanual))])
    #     else:
    #         _, __, new_item_df, _ = wf_util.tab_replace_null('GenerateUserProfile', with_context, item_df, None, [('UPAutomatic', str(upauto)), ('UPManual', str(upmanual))])
    
    # # TAB --> User Profile:
    # user_profile_df = pd.DataFrame()
    # with tab_generate_user_profile:
    #     # Generating the user profile manually:
    #     if up_option == 'Manual':  
    #         # Help information:
    #         help_information.help_user_profile_manual()
    #         if with_context:           
    #             if not item_df.empty and not context_df.empty:
    #                 # Adding column "id":
    #                 attribute_column_list = ['user_profile_id']  
    #                 # Adding relevant item attribute columns:        
    #                 item_access = AccessItem(item_df)
    #                 item_attribute_name_list = item_access.get_item_attribute_list()                
    #                 attribute_column_list.extend(item_attribute_name_list)   
    #                 item_possible_value_map = {}     
    #                 for item_attribute_name in item_attribute_name_list:
    #                     item_possible_value_map[item_attribute_name] = item_access.get_item_possible_value_list_from_attributte(attribute_name=item_attribute_name)
    #                 # Adding relevant context attribute columns:    
    #                 context_access = AccessContext(context_df)
    #                 context_attribute_name_list = context_access.get_context_attribute_list()                    
    #                 attribute_column_list.extend(context_attribute_name_list)
    #                 context_possible_value_map = {}
    #                 for context_attribute_name in context_attribute_name_list:
    #                     context_possible_value_map[context_attribute_name] = context_access.get_context_possible_value_list_from_attributte(attribute_name=context_attribute_name)
    #                 # Adding column "other":
    #                 attribute_column_list.extend(['other'])
    #                 # Introducing the number of user profiles to generate:   
    #                 number_user_profile = st.number_input(label='Number of user profiles', value=4)
    #                 # Generate user profile manual (with context):              
    #                 user_profile_df = wf_util.generate_user_profile_manual(number_user_profile, attribute_column_list, item_possible_value_map, context_possible_value_map)
    #             else:
    #                 st.warning("The item and context files have not been uploaded.")
    #         else:              
    #             if not item_df.empty:
    #                 # Adding column "id":
    #                 attribute_column_list = ['user_profile_id']  
    #                 # Adding relevant item attribute columns:        
    #                 item_access = AccessItem(item_df)
    #                 item_attribute_name_list = item_access.get_item_attribute_list()                
    #                 attribute_column_list.extend(item_attribute_name_list)   
    #                 item_possible_value_map = {}     
    #                 for item_attribute_name in item_attribute_name_list:
    #                     item_possible_value_map[item_attribute_name] = item_access.get_item_possible_value_list_from_attributte(attribute_name=item_attribute_name)
    #                 # Adding column "other":
    #                 attribute_column_list.extend(['other'])
    #                 # Introducing the number of user profiles to generate:   
    #                 number_user_profile = st.number_input(label='Number of user profiles', value=4)
    #                 # Generate user profile manual (not context):                 
    #                 user_profile_df = wf_util.generate_user_profile_manual(number_user_profile, attribute_column_list, item_possible_value_map)
    #             else:
    #                 st.warning("The item file has not been uploaded.")
    #     elif up_option == 'Automatic':
    #         # Help information:
    #         help_information.help_user_profile_automatic()            
    #         if with_context:
    #             # Generate user profile automatic (with context):               
    #             if (not new_item_df.empty) and (not new_context_df.empty) and (not rating_df.empty):
    #                 user_profile_df = wf_util.generate_user_profile_automatic(rating_df, new_item_df, new_context_df)
    #                 st.dataframe(user_profile_df)
    #             else:
    #                 st.warning("The item, context and rating files have not been uploaded.")
    #         else:
    #             # Generate user profile automatic (not context):                     
    #             if (not new_item_df.empty) and (not rating_df.empty):
    #                 user_profile_df = wf_util.generate_user_profile_automatic(rating_df, new_item_df)
    #                 st.dataframe(user_profile_df)
    #             else:
    #                 st.warning("The item and rating files have not been uploaded.")

# def generate_user_profile_automatic(rating_df, item_df, context_df=None):
#     """
#     """
#     try:
#         output = st.empty()
#         with console.st_log(output.code):
#             # Generate user profile, by using an original dataset:
#             generate_up_dataset = None
#             user_profile_df = pd.DataFrame()                    
#             if context_df is not None and not context_df.empty:                     
#                 # With context:            
#                 if (not item_df.empty) and (not context_df.empty) and (not rating_df.empty):
#                         if st.button(label='Generate', key='button_generate_up_cars'):
#                             print('Automatically generating user profiles.')                    
#                             generate_up_dataset = GenerateUserProfileDataset(rating_df, item_df, context_df)
#                             user_profile_df = generate_up(generate_up_dataset)                                  
#                             print('The user profile has been generated.')                                                    
#                 else:
#                     st.warning("The item, context and rating files have not been uploaded.")
#             else:
#                 # Without context:            
#                 if (not item_df.empty) and (not rating_df.empty): 
#                     if st.button(label='Generate', key='button_generate_up_rs'):
#                         print('Automatically generating user profiles.')                    
#                         generate_up_dataset = GenerateUserProfileDataset(rating_df, item_df)
#                         user_profile_df = generate_up(generate_up_dataset)                    
#                         print('The user profile has been generated.')
#                 else:
#                     st.warning("The item and rating files have not been uploaded.")
#     except Exception:
#         # Generate user profile, by using an original dataset:
#         generate_up_dataset = None
#         user_profile_df = pd.DataFrame()                    
#         if context_df is not None and not context_df.empty:                     
#             # With context:            
#             if (not item_df.empty) and (not context_df.empty) and (not rating_df.empty):
#                 print('Automatically generating user profiles.')                    
#                 generate_up_dataset = GenerateUserProfileDataset(rating_df, item_df, context_df)
#                 user_profile_df = generate_up(generate_up_dataset)                                  
#                 print('The user profile has been generated.')                                                    
#             else:
#                 print("The item, context and rating files have not been uploaded.")
#         else:
#             # Without context:            
#             if (not item_df.empty) and (not rating_df.empty): 
#                     print('Automatically generating user profiles.')                    
#                     generate_up_dataset = GenerateUserProfileDataset(rating_df, item_df)
#                     user_profile_df = generate_up(generate_up_dataset)                    
#                     print('The user profile has been generated.')
#             else:
#                 print("The item and rating files have not been uploaded.")
#     return user_profile_df

# def generate_user_profile_automatic():
#     pass
