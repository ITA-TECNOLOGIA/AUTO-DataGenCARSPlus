import streamlit as st
import config


####### Generate a synthetic dataset ######
def help_explicit_rating_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate a completely-synthetic dataset based on explicit ratings.""")

def help_implicit_rating_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate a completely-synthetic dataset based on implicit ratings.""")

####### Pre-process a dataset #######
# LOAD DATASET:

# WORKFLOW:
# Replicate dataset:
def help_replicate_dataset_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate a synthetic dataset similar to an existing one.""")

# Extend dataset:
def help_extend_dataset_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate a dataset of ratings incrementally.""")

# Recalculate ratings:
def help_recalculate_ratings_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to recalculate ratings in a dataset.""")

# Replace NULL values:
def help_replace_nulls_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to complete unknown contextual information.""")

# Generate user profile:
def help_user_profile_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate an user profile automatically or manually.""")

def help_user_profile_manual():
    with st.expander(label='Help information'):
        st.markdown("""Insert weight values in the user profile matrix, considering the following:""")            
        st.markdown("""* First of all, you will have to specify the ```number of user profiles``` to be generated. """)
        st.markdown("""* The user profile matrix consists of relevant attribute names related to the items and/or contexts. """)
        st.markdown("""* The values of the user profile matrix must have values between ```[0-1]```. Except column ```user_profile_id``` which must be an ```integer``` value and start at ```1```. """)
        st.markdown("""* Attributes that are not relevant for the user profile must have a ```weight=0```. """)
        st.markdown("""* Each row of the user profile matrix must sum to ```1```. """)
        st.markdown("""* In the ```row``` and ```column``` input fields, you must indicate the row index and the column attribute name (respectively), where the user's relevance weight will be inserted through the ```weight``` field. """)            
        st.markdown("""* In the ```weight``` input field, you must indicate the order and weight of importance of each attribute. For example:  ```(-)|0.1``` or ```(+)|0.1)```. """)                
        st.markdown(
        """
        * Weights may be associated with symbols or labels ```(-)``` and ```(+)```, which indicate the order of preference of attribute values for that user profile. The ```(-)``` label must indicate that the order of preference of the attribute values is from left to right, while the ```(+)``` label indicates the reverse order of preference (from right to left). For example, for the attribute ```distance``` and possible values ```[near, fear]```: 
        * **Example 1:** If the user indicates the label ``(-)``, it means that he/she prefers recommendations of nearby places (because he/she does not have a car or a bicycle or a bus as a means of transport to go to distant places).
        * **Example 2:** If the user indicates the label ``(+)``, it means that he does not mind receiving recommendations from places far away from him/ (because he has a car as a means of transport to go to distant places).
        """)
        st.markdown(
        """
        * The special attribute ```other``` represents unknown factors or noise. This allows modelling realistic scenarios where user profiles are not fully defined. For example:
        * **Example 1:** The user with ```user_profile_id=2```,  with a ```weight=0.2``` in the attribute ```other```, considers that ```20%``` of the ratings provided by the user of that profile, is due to unknown factors. 
        * **Example 2:** The user with ```user_profile_id=3```, with a ```weight=1``` in the attribute ```other```, represents users who behave in a completely unpredictable way. This is because the ratings provided by users cannot be explained by any of the attributes that define the user profile. """)
        st.write('Example of user profile matrix:')
        st.image(image=config.USER_PROFILE, use_column_width=True, output_format="auto")

def help_user_profile_automatic():
    with st.expander(label='Help information'):
        st.markdown("""Generates user profiles automatically. A profile will be generated for each user. For that, the [LSMR](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.lsmr.html) method (An Iterative Algorithm for Sparse Least-Squares Problems) was used.""")
        st.markdown("""The resulting user profile matrix is described below:""")
        st.markdown("""* The user profile matrix consists of relevant attribute names related to the items and/or contexts. """)
        st.markdown("""* The values of the user profile matrix have values between ```[0-1]```. Except column ```user_profile_id``` which is an ```integer``` value and start at ```1```. """)
        st.markdown("""* Attributes that are not relevant for the user profile have a ```weight=0```. """)
        st.markdown("""* Each row of the user profile matrix sum to ```1```. """)        
        st.markdown(
        """
        * Weights are associated with symbols or labels ```(-)``` and ```(+)```, which indicate the order of preference of attribute values for that user profile. The ```(-)``` label must indicate that the order of preference of the attribute values is from left to right, while the ```(+)``` label indicates the reverse order of preference (from right to left). For example, for the attribute ```distance``` and possible values ```[near, fear]```: 
        * **Example 1:** If the user indicates the label ``(-)``, it means that he/she prefers recommendations of nearby places (because he/she does not have a car or a bicycle or a bus as a means of transport to go to distant places).
        * **Example 2:** If the user indicates the label ``(+)``, it means that he does not mind receiving recommendations from places far away from him/ (because he has a car as a means of transport to go to distant places).
        """)
        st.markdown(
        """
        * The special attribute ```other``` represents unknown factors or noise. This allows modelling realistic scenarios where user profiles are not fully defined. For example:
        * **Example 1:** The user with ```user_profile_id=2```,  with a ```weight=0.2``` in the attribute ```other```, considers that ```20%``` of the ratings provided by the user of that profile, is due to unknown factors. 
        * **Example 2:** The user with ```user_profile_id=3```, with a ```weight=1``` in the attribute ```other```, represents users who behave in a completely unpredictable way. This is because the ratings provided by users cannot be explained by any of the attributes that define the user profile. """)
        st.write('Example of user profile matrix:')
        st.image(image=config.USER_PROFILE, use_column_width=True, output_format="auto")

# Ratings to binary:
def help_ratings_to_binary_wf():
    with st.expander(label='Help information'):
        st.markdown("""This tool allows you to convert ratings to binary values. For example, if you have a dataset with ratings from ```1``` to ```5```, you can convert them to ```0``` and ```1```, where ```0``` represents a negative rating and ```1``` a positive one.""")
        st.markdown("""The tool will convert the ratings to binary values using a threshold. For example, if you set the threshold to ```3```, all ratings equal or greater than ```3``` will be converted to ```1```, and all ratings less than ```3``` will be converted to ```0```.""")

# Mapping categorization:
def help_mapping_categorization_wf():
    with st.expander(label='Help information'):
        st.markdown("""TODO""")

def help_mapping_categorization_num2cat():
    with st.expander(label='Help information'):
        st.markdown("""This workflow allows you to convert numerical values to categorical values. For example, you can convert the numerical values of a rating scale to the corresponding categories of the scale (e.g. ```1-2 -> Bad```, ```3-4 -> Average```, ```5 -> Good```).""")
        st.markdown("""To use this tool, you need to upload a CSV file containing the numerical values to convert. Then, you need to specify the mapping for each numerical value. For example, you could to specify the following mappings: numerical values ```1```, ```2```, ```3```, ```4``` and ```5``` to categories ```Bad```, ```Average```, ```Good```, ```Very good``` and ```Excellent```, respectively.""")
        st.markdown("""Objects and datetime values are ignored.""")   

def help_mapping_categorization_cat2num():
    with st.expander(label='Help information'):
        st.markdown("""This workflow allows you to convert categorical values into numerical values.""")
        st.markdown("""For example, you can convert the categorical values of a rating scale to the corresponding numerical values of the scale (e.g. ```Bad -> 1```, ```Average -> 2```, ```Good -> 3```, ```Very good -> 4```, ```Excellent -> 5```).""")
        st.markdown("""To use this tool, you need to upload a CSV file containing the categorical values to convert. Then, you need to select the categorical columns to convert.""")

####### Analysis a dataset #######
# VISUALIZATION:
# EVALUATION: