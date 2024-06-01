from io import BytesIO
import os
from zipfile import ZipFile
import streamlit as st
from streamlit_app import config


####### Generate a synthetic dataset ######
def help_explicit_rating_rs_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate a completely-synthetic dataset based on explicit ratings.""")    
        
        st.markdown("""**Example video:**""")
        help_video_from_url(video_url=config.SYNTHETIC_DATASET_VIDEO_EXPLICIT_RS_URL, title_video='Generate a synthetic dataset for evaluation of traditional RS based on explicit ratings')        
        st.markdown("""**Example dataset:**""")
        st.download_button(label=f"{config.RESTAURANT_SCHEMA_EXPLICIT_RS_NAME}.zip", data=get_zip_file(config.RESTAURANT_SCHEMA_EXPLICIT_RS_PATH), file_name=f"{config.RESTAURANT_SCHEMA_EXPLICIT_RS_NAME}.zip", mime="application/zip")
        
def help_explicit_rating_cars_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate a completely-synthetic dataset based on explicit ratings.""")    
        
        st.markdown("""**Example video:**""")
        help_video_from_url(video_url=config.SYNTHETIC_DATASET_VIDEO_EXPLICIT_CARS_URL, title_video='Generate a synthetic dataset for evaluation of CARS based on explicit ratings')        
        st.markdown("""**Example dataset:**""")
        st.download_button(label=f"{config.RESTAURANT_SCHEMA_EXPLICIT_CARS_NAME}.zip", data=get_zip_file(config.RESTAURANT_SCHEMA_EXPLICIT_CARS_PATH), file_name=f"{config.RESTAURANT_SCHEMA_EXPLICIT_CARS_NAME}.zip", mime="application/zip")
        
def help_implicit_rating_rs_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate a completely-synthetic dataset based on implicit ratings.""")    
        
        st.markdown("""**Example video:**""")
        help_video_from_url(video_url=config.SYNTHETIC_DATASET_VIDEO_IMPLICIT_RS_URL, title_video='Generate a synthetic dataset for evaluation of traditional RS based on implicit ratings')        
        st.markdown("""**Example dataset:**""")
        st.download_button(label=f"{config.RESTAURANT_SCHEMA_IMPLICIT_RS_NAME}.zip", data=get_zip_file(config.RESTAURANT_SCHEMA_IMPLICIT_RS_PATH), file_name=f"{config.RESTAURANT_SCHEMA_IMPLICIT_RS_NAME}.zip", mime="application/zip")
        
def help_implicit_rating_cars_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate a completely-synthetic dataset based on implicit ratings.""")    
        
        st.markdown("""**Example video:**""")
        help_video_from_url(video_url=config.SYNTHETIC_DATASET_VIDEO_IMPLICIT_CARS_URL, title_video='Generate a synthetic dataset for evaluation of CARS based on implicit ratings')        
        st.markdown("""**Example dataset:**""")
        st.download_button(label=f"{config.RESTAURANT_SCHEMA_IMPLICIT_CARS_NAME}.zip", data=get_zip_file(config.RESTAURANT_SCHEMA_IMPLICIT_CARS_PATH), file_name=f"{config.RESTAURANT_SCHEMA_IMPLICIT_CARS_NAME}.zip", mime="application/zip")

def help_schema_file():
    with st.expander(label='Help information'):
        st.write('Different types of generators can be used:')
        st.markdown("""- **Categorical**: It generates a random value (a ```string``` value from an list, or a ```boolean``` value, depending on the domain of the specific attribute). Random values are by default generated according to a ```uniform probabilistic distribution```, but it is possible to parametrize to use a ```gaussian distribution```. """)
        st.markdown("""- **Numerical**: It generates a random value (an ```integer``` or ```float``` value in a given range, depending on the domain of the specific attribute). Random values are by default generated according to a ```uniform probabilistic distribution```, but it is possible to parametrize to use a ```gaussian distribution```. """)
        st.markdown("""- **Fixed**: It generates fiexed values. For example, if you want the ```country``` attribute to always have the same value of ```Spain``` for all its instances.""")
        st.markdown("""- **Date**: It allows generating random dates within a certain range of years required. """)
        st.markdown("""- **BooleanList**: It generates an array of boolean values representing the presence or absence of a certain feature or Component (e.g., it fills with true/false the opening days of a business—```Monday```, ```Tuesday```, ```Wednesday```, ```Thursday```, ```Friday```, ```Saturday```, ```Sunday```—or the types of foods served in a restaurant—```Italian```, ```Mexican```, ```etc```., based on the average percentage of true values desired). """)
        st.markdown("""- **URL**: It generates ```URL``` of web pages, by collecting place name values from an input data provided.""")
        st.markdown("""- **Address**: It generates consistent values for typical attributes representing an address(```street```, ```number```, ```ZIP code```, ```latitude```, and ```longitude```) by collecting these values from an input data provided. """)
        st.markdown("""- **Device**: It generates features of an informatic ```device``` (e.g., ```mobile phone```, ```computer```, ```tablet```, etc.) comprising five sub-attributes: ```browser name```, ```browser version```, ```device type```, ```operating system name```, ```operating system version```. Each sub-attribute is of the String type, with certain sub-attributes having specified input parameters that determine their possible values. For example, ```{'browserName': 'Chrome', 'browserVersion': '88.8378.8638.9531', 'deviceType': 'browser', 'osName': 'iOS', 'osVersion': '11.4.7'}```. """)        
        st.markdown("""- **Position**: It generates item or user positions. The attribute value represents the three-dimensional coordinates of the user or item in a 3D space. It is a compound of three sub-attributes, ```longitude (x)```, ```latitude (y)```, and ```altitude (z)```. """)

def help_implicit_rating_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate a completely-synthetic dataset based on implicit ratings.""")

def help_important_attribute_ranking_order():
    st.write('Examples of importance order:')
    st.markdown("""- ascending: ``` quality food=[bad, normal, good], global_rating=[1, 5], card=[False, True] ``` """)
    st.markdown("""- descending: ``` quality food=[good, normal, bad], global_rating=[5, 1], card=[True, False] ``` """)
    st.markdown("""- neutral (no important order): ``` quality food=[chinese, italian, vegetarian, international] ``` """)

def help_overlapping_attribute_values():
    st.markdown(
    """ 
    ```python
    # Example 1: overlapping at the midpoint on the left and the right
    item_profile_names = ['bad', 'normal', 'good'] 
    overlap_midpoint_left_profile = 0 
    overlap_midpoint_right_profile = 0 
    good_profile =   ['good'] 
    normal_profile =   ['normal'] 
    bad_profile =   ['bad'] 
    ``` 
    """)
    st.markdown(""" 
    ```python
    # Example 2: overlapping at the midpoint on the left and the right
    item_profile_names = ['bad', 'normal', 'good']
    overlap_midpoint_left_profile = 1
    overlap_midpoint_right_profile = 1
    good_item_profile =   ['good']
    normal_item_profile =   ['bad', 'normal', 'good']
    bad_item_profile =   ['bad']
    ``` 
    """)

def help_user_profile_id():
    st.markdown(""" Please, note that the ```user_profile_id``` column must start at ```1```, while the rest of values must be in the range ```[-1,1]```.""")

####### Pre-process a dataset #######
# WORKFLOWS:
# WF --> Replace NULL values:
def help_replace_nulls_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to complete unknown contextual information.""")

# WF --> Generate NULL values:
def help_generate_nulls_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate a percentage with unknown contextual information.""")

# WF --> Replicate dataset:
def help_replicate_dataset_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate a synthetic dataset similar to an existing one.""")

# WF --> Extend dataset:
def help_extend_dataset_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate a dataset of ratings incrementally.""")

# WF --> Recalculate ratings:
def help_recalculate_ratings_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to recalculate ratings in a dataset.""")

# WF --> Generate user profile:
def help_user_profile_wf():
    with st.expander(label='Help information'):
        st.markdown("""Workflow to generate an user profile automatically or manually.""")

def help_user_profile_manual():
    with st.expander(label='Help information'):
        st.markdown("""Insert weight values in the user profile matrix, considering the following:""")            
        st.markdown("""* If the ```user_profile_id``` column is not present in the ```user.csv``` file, you will have to specify the ```number of user profiles``` to be generated. """)
        st.markdown("""* The user profile matrix consists of relevant attribute names related to the items and/or contexts. """)
        st.markdown("""* The values of the user profile matrix must have values between ```[0-1]```. Except column ```user_profile_id``` which must be an ```integer``` value and start at ```1```. """)
        st.markdown("""* Attributes that are not relevant for the user profile must have a ```weight=0```. """)
        st.markdown("""* Each row of the user profile matrix must sum to ```1```. """)
        st.markdown("""* In the cells of the dataframe, you must insert the ```weight``` value and the order of importance of each attribute. For example:  ```-0.1``` --> ```(-)|0.1``` or ```0.1``` --> ```(+)|0.1)```. """)
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
        st.image(image=config.USER_PROFILE_IMAGE, use_column_width=True, output_format="auto")

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
        st.image(image=config.USER_PROFILE_IMAGE, use_column_width=True, output_format="auto")

# WF --> Cast rating:
def help_cast_rating_wf():
    with st.expander(label='Help information'):
        st.markdown("""This tool allows you to cast your vote by applying one of the following strategies:""")
        st.markdown(""" - **Preferencial to Binary**: Transforms ratings based on value ranges (e.g., [1-5]) to binary values (e.g., [0-1]), by applying a threshold. For example, if you have a dataset with ratings from ```1``` to ```5```, you can convert them to ```0``` and ```1```, where ```0``` represents a negative rating and ```1``` a positive one.""")
        st.markdown(""" - **Binary to Preferencial**:  Transforms binary ratings (0/1) to preferential ratings (1-5) based on a specified scale and theshold.""")
        
# WF --> Data converter:
def help_data_converter_wf():
    with st.expander(label='Help information'):
        st.markdown(""" Converts data between numerical and categorical representations. """)

def help_numerical_to_categorical():
    with st.expander(label='Help information'):
        st.markdown("""This workflow allows you to convert numerical values to categorical values. For example, you can convert the numerical values of a rating scale to the corresponding categories of the scale (e.g. ```1-2 -> Bad```, ```3-4 -> Average```, ```5 -> Good```).""")
        st.markdown("""To use this tool, you need to upload a CSV file containing the numerical values to convert. Then, you need to specify the mapping for each numerical value. For example, you could to specify the following mappings: numerical values ```1```, ```2```, ```3```, ```4``` and ```5``` to categories ```Bad```, ```Average```, ```Good```, ```Very good``` and ```Excellent```, respectively.""")
        st.markdown("""Objects and datetime values are ignored.""")   

def help_categorical_to_numerical():
    with st.expander(label='Help information'):
        st.markdown("""This workflow allows you to convert categorical values into numerical values.""")
        st.markdown("""For example, you can convert the categorical values of a rating scale to the corresponding numerical values of the scale (e.g. ```Bad -> 1```, ```Average -> 2```, ```Good -> 3```, ```Very good -> 4```, ```Excellent -> 5```).""")
        st.markdown("""To use this tool, you need to upload a CSV file containing the categorical values to convert. Then, you need to select the categorical columns to convert.""")

####### Analysis of a dataset #######
# VISUALIZATION:
def help_visualization_dataset_explicit_rs():
    with st.expander(label='Help information'):
        st.markdown("""Visualization of a dataset.""")   
        st.markdown("""**Example video:**""")     
        help_video_from_url(video_url=config.VISUALIZATION_PREFERENCIAL_EXPLICIT_RS_URL, title_video='Visualization of a RS dataset with preferencial and explicit ratings')        
        st.markdown("""**Example datasets:**""")
        st.download_button(label=f"{config.STS_DATASET_PREFERENCIAL_EXPLICIT_RS_NAME}.zip", data=get_zip_file(config.STS_DATASET_PREFERENCIAL_EXPLICIT_RS_PATH), file_name=f"{config.STS_DATASET_PREFERENCIAL_EXPLICIT_RS_NAME}.zip", mime="application/zip")        
        st.download_button(label=f"{config.STS_DATASET_BINARY_EXPLICIT_RS_NAME}.zip", data=get_zip_file(config.STS_DATASET_BINARY_EXPLICIT_RS_PATH), file_name=f"{config.STS_DATASET_BINARY_EXPLICIT_RS_NAME}.zip", mime="application/zip")

def help_visualization_dataset_explicit_cars():
    with st.expander(label='Help information'):
        st.markdown("""Visualization of a dataset.""")
        st.markdown("""**Example video:**""")
        help_video_from_url(video_url=config.VISUALIZATION_PREFERENCIAL_EXPLICIT_CARS_URL, title_video='Visualization of a CARS dataset with preferencial and explicit ratings')        
        st.markdown("""**Example datasets:**""")
        st.download_button(label=f"{config.STS_DATASET_PREFERENCIAL_EXPLICIT_CARS_NAME}.zip", data=get_zip_file(config.STS_DATASET_PREFERENCIAL_EXPLICIT_CARS_PATH), file_name=f"{config.STS_DATASET_PREFERENCIAL_EXPLICIT_CARS_NAME}.zip", mime="application/zip")        
        st.download_button(label=f"{config.STS_DATASET_BINARY_EXPLICIT_CARS_NAME}.zip", data=get_zip_file(config.STS_DATASET_BINARY_EXPLICIT_CARS_PATH), file_name=f"{config.STS_DATASET_BINARY_EXPLICIT_CARS_NAME}.zip", mime="application/zip")

def help_visualization_dataset_implicit_rs():
    with st.expander(label='Help information'):
        st.markdown("""Visualization of a dataset.""")   
        st.markdown("""**Example video:**""")  
        help_video_from_url(video_url=config.VISUALIZATION_PREFERENCIAL_IMPLICIT_RS_URL, title_video='Visualization of a RS dataset with preferencial and implicit ratings')        
        st.markdown("""**Example datasets:**""")
        st.download_button(label=f"{config.STS_DATASET_PREFERENCIAL_IMPLICIT_RS_NAME}.zip", data=get_zip_file(config.STS_DATASET_PREFERENCIAL_IMPLICIT_RS_PATH), file_name=f"{config.STS_DATASET_PREFERENCIAL_IMPLICIT_RS_NAME}.zip", mime="application/zip")        
        st.download_button(label=f"{config.STS_DATASET_BINARY_IMPLICIT_RS_NAME}.zip", data=get_zip_file(config.STS_DATASET_BINARY_IMPLICIT_RS_PATH), file_name=f"{config.STS_DATASET_BINARY_IMPLICIT_RS_NAME}.zip", mime="application/zip")

def help_visualization_dataset_implicit_cars():
    with st.expander(label='Help information'):
        st.markdown("""Visualization of a dataset.""")
        st.markdown("""**Example video:**""") 
        help_video_from_url(video_url=config.VISUALIZATION_PREFERENCIAL_IMPLICIT_CARS_URL, title_video='Visualization of a CARS dataset with preferencial and implicit ratings')        
        st.markdown("""**Example datasets:**""")
        st.download_button(label=f"{config.STS_DATASET_PREFERENCIAL_IMPLICIT_CARS_NAME}.zip", data=get_zip_file(config.STS_DATASET_PREFERENCIAL_IMPLICIT_CARS_PATH), file_name=f"{config.STS_DATASET_PREFERENCIAL_IMPLICIT_CARS_NAME}.zip", mime="application/zip")        
        st.download_button(label=f"{config.STS_DATASET_BINARY_IMPLICIT_CARS_NAME}.zip", data=get_zip_file(config.STS_DATASET_BINARY_IMPLICIT_CARS_PATH), file_name=f"{config.STS_DATASET_BINARY_IMPLICIT_CARS_NAME}.zip", mime="application/zip")
        
# EVALUATION:    
def help_rs_algoritms(recommender_name_list):
    with st.expander(label='Help information'):    
        st.markdown("""Evaluation of a RS using the following Collaborative Filtering techniques:""")                                           
        for recommender_name in recommender_name_list:                        
            # Basic algorithms:
            if recommender_name == 'NormalPredictor':
                st.markdown("""- ``` NormalPredictor ```: Algorithm predicting a random rating based on the distribution of the training set, which is assumed to be normal.""")
            if recommender_name == 'BaselineOnly':
                st.markdown("""
                            - ``` BaselineOnly ```: Algorithm predicting the baseline estimate for given user and item.                
                            Parameter settings: 
                                > - ```method```: The method to use for baseline estimates. Options include 'als' (Alternating Least Squares) or 'sgd' (Stochastic Gradient Descent). The default is 'als'. 
                                > - ```reg_i```: Regularization parameter for items. Controls the degree of regularization applied to item biases. Default is 10.
                                > - ```reg_u```: Regularization parameter for users. Controls the degree of regularization applied to user biases. Default is 15.
                                > - ```n_epochs```: The number of iterations for optimization algorithms (e.g., SGD). Default is 10.
                                > - ```learning_rate```: Learning rate for optimization algorithms (SGD). Default is 0.005.
                            """)           
            # KNN-based CF algorithms:
            if recommender_name == 'KNNBasic':                              
                st.markdown("""
                            - ``` KNNBasic ```: A basic collaborative filtering algorithm derived from a basic nearest neighbors approach.
                            Parameter settings:
                                > - ```k```: The number of neighbors to consider when making predictions. Typical value range: 1 to 100. The default is 40. 
                                > - ```min_k```: The minimum number of neighbors required for a prediction to be computed. If there are fewer neighbors, the prediction may be set to a global mean. Typical value range: 1 to 10. Default is 1.
                                > - ```name```: The similarity measure to use, e.g., 'cosine', 'pearson', 'msd' (mean squared difference), etc.
                                > - ```user_based```: A boolean indicating whether to use user-based or item-based similarity.     
                                > - ```min_support```: Minimum number of common items/users required to compute similarity.
                            """)            
            if recommender_name == 'KNNBaseline':                
                st.markdown("""
                            - ``` KNNBaseline ```: A basic collaborative filtering algorithm taking into account a baseline rating.
                            Parameter settings:
                                > - ```k```: The number of neighbors to consider when making predictions. Typical value range: 1 to 100. The default is 40. 
                                > - ```min_k```: The minimum number of neighbors required for a prediction to be computed. If there are fewer neighbors, the prediction may be set to a global mean. Typical value range: 1 to 10. Default is 1.
                                > - ```name```: The similarity measure to use, e.g., 'cosine', 'pearson', 'msd' (mean squared difference), etc.
                                > - ```user_based```: A boolean indicating whether to use user-based or item-based similarity.                            
                                > - ```method```: The method to use for baseline estimates. Options include 'als' (Alternating Least Squares) or 'sgd' (Stochastic Gradient Descent). The default is 'als'. 
                                > - ```reg_i```: Regularization parameter for items. Controls the degree of regularization applied to item biases. Default is 10.
                                > - ```reg_u```: Regularization parameter for users. Controls the degree of regularization applied to user biases. Default is 15.
                                > - ```n_epochs```: The number of iterations for optimization algorithms (e.g., SGD). Default is 10.
                                > - ```learning_rate```: Learning rate for optimization algorithms (SGD). Default is 0.005.
                            """)                 
            if recommender_name == 'KNNWithMeans':
                st.markdown("""
                            - ``` KNNWithMeans ```: A basic collaborative filtering algorithm, taking into account the mean ratings of each user.
                            Parameter settings:
                                > - ```k```: The number of neighbors to consider when making predictions. Typical value range: 1 to 100. The default is 40. 
                                > - ```min_k```: The minimum number of neighbors required for a prediction to be computed. If there are fewer neighbors, the prediction may be set to a global mean. Typical value range: 1 to 10. Default is 1.
                                > - ```name```: The similarity measure to use, e.g., 'cosine', 'pearson', 'msd' (mean squared difference), etc.
                                > - ```user_based```: A boolean indicating whether to use user-based or item-based similarity.     
                                > - ```min_support```: Minimum number of common items/users required to compute similarity.
                            """)
            if recommender_name == 'KNNWithZScore':
                st.markdown("""
                            - ``` KNNWithZScore ```: A basic collaborative filtering algorithm, taking into account the z-score normalization of each user.
                            Parameter settings:
                                > - ```k```: The number of neighbors to consider when making predictions. Typical value range: 1 to 100. The default is 40. 
                                > - ```min_k```: The minimum number of neighbors required for a prediction to be computed. If there are fewer neighbors, the prediction may be set to a global mean. Typical value range: 1 to 10. Default is 1.
                                > - ```name```: The similarity measure to use, e.g., 'cosine', 'pearson', 'msd' (mean squared difference), etc.
                                > - ```user_based```: A boolean indicating whether to use user-based or item-based similarity.     
                                > - ```min_support```: Minimum number of common items/users required to compute similarity.
                            """)            
            
            # Matrix factorization-based CF algorithms:
            if recommender_name == 'SVD':
                st.markdown("""
                            - ``` SVD ```: The famous SVD algorithm, as popularized by Simon Funk during the Netflix Prize. When baselines are not used, this is equivalent to Probabilistic Matrix Factorization.
                            Parameter settings:
                                > - ```n_factors```: Number of latent factors to use in the matrix factorization. Default is 20.
                                > - ```n_epochs```: Number of epochs the algorithm should run during training. Each epoch involves one pass over the entire training dataset. Default is 20.
                                > - ```lr_all```: The learning rate used for Stochastic Gradient Descent (SGD) optimization during training. It controls the step size in updating the model's parameters in each iteration. Default is 0.007.
                                > - ```reg_all```: The regularization term applied to all parameters during training. It helps prevent overfitting by penalizing large parameter values. Default is 0.02.
                                > - ```biased```: Whether to use baselines (or biases). Default is True.
                                > - ```init_mean```: The mean of the normal distribution for factor vectors initialization. Default is 0.
                                > - ```init_std_dev```: The standard deviation of the normal distribution for factor vectors initialization. Default is 0.1.
                            """)
            if recommender_name == 'SVDpp':
                st.markdown("""
                            - ``` SVDpp ```: The SVD++ algorithm, an extension of SVD taking into account implicit ratings.
                            Parameter settings:
                                > - ```n_factors```: Number of latent factors to use in the matrix factorization. Default is 20.
                                > - ```n_epochs```: Number of epochs the algorithm should run during training. Each epoch involves one pass over the entire training dataset. Default is 20.
                                > - ```lr_all```: The learning rate used for Stochastic Gradient Descent (SGD) optimization during training. It controls the step size in updating the model's parameters in each iteration. Default is 0.007.
                                > - ```reg_all```: The regularization term applied to all parameters during training. It helps prevent overfitting by penalizing large parameter values. Default is 0.02.                                
                                > - ```init_mean```: The mean of the normal distribution for factor vectors initialization. Default is 0.
                                > - ```init_std_dev```: The standard deviation of the normal distribution for factor vectors initialization. Default is 0.1.
                            """)
            if recommender_name == 'NMF':
                st.markdown("""
                            - ``` NMF ```:  A collaborative filtering algorithm based on Non-negative Matrix Factorization.
                            Parameter settings:
                                > - ```n_factors```: Number of latent factors to use in the matrix factorization. Default is 15.
                                > - ```n_epochs```: Number of epochs of the SGD procedure. Default is 50.
                                > - ```biased```: Whether to use baselines (or biases)". Default is False.
                                > - ```reg_pu```: Regularization term for user factors. Default is 0.06.
                                > - ```reg_qi```: Regularization term for item factors. Default is 0.06.
                                > - ```reg_bu```: Regularization term for bu. Only relevant for biased version. Default is 0.02.
                                > - ```reg_bi```: Regularization term for bi. Only relevant for biased version. Default is 0.02.
                                > - ```lr_bu```: The learning rate for bu. Only relevant for biased version. Default is 0.005.
                                > - ```lr_bi```: The learning rate for bi. Only relevant for biased version. Default is 0.005
                                > - ```init_low```: Lower bound for random initialization of factors. Must be greater than 0 to ensure non-negative factors. Default is 0.
                                > - ```init_high```: Higher bound for random initialization of factors. Default is 1.
                            """)
            
            # Clustering-based CF algorithms:
            if recommender_name == 'CoClustering':
                st.markdown("""
                            - ``` CoClustering ```: A collaborative filtering algorithm based on co-clustering. This is a straightforward implementation of [GM05]. [GM05] Thomas George and Srujana Merugu. [A scalable collaborative filtering framework based on co-clustering](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.113.6458&rep=rep1&type=pdf). 2005.
                            Parameter settings:
                                > - ```n_cltr_u```: Number of user clusters. Default is 3.
                                > - ```n_cltr_i```: Number of item clusters. Default is 3.
                                > - ```n_epochs```: Number of iteration of the optimization loop. Default is 20.
                            """)
            
            if recommender_name == 'SlopeOne':
                st.markdown("""
                            - ``` SlopeOne ```: A simple yet accurate collaborative filtering algorithm. This is a straightforward implementation of the SlopeOne algorithm [LM07]. [LM07] Daniel Lemire and Anna Maclachlan. [Slope one predictors for online rating-based collaborative filtering](https://arxiv.org/abs/cs/0702144). 2007.
                            """)
        st.markdown("""These algorithms are implemented in the [surprise](https://github.com/NicolasHug/Surprise) python library.""")
        
        st.markdown("""**Example video:**""")
        help_video_from_url(video_url=config.EVALUATION_PREFERENCIAL_RS_URL, title_video='Evaluation of a traditional RS dataset using preferencial and explicit ratings')        
        st.markdown("""**Example datasets:**""")
        st.download_button(label=f"{config.STS_DATASET_PREFERENCIAL_EXPLICIT_RS_NAME}.zip", data=get_zip_file(config.STS_DATASET_PREFERENCIAL_EXPLICIT_RS_PATH), file_name=f"{config.STS_DATASET_PREFERENCIAL_EXPLICIT_RS_NAME}.zip", mime="application/zip")        
        st.download_button(label=f"{config.STS_DATASET_BINARY_EXPLICIT_RS_NAME}.zip", data=get_zip_file(config.STS_DATASET_BINARY_EXPLICIT_RS_PATH), file_name=f"{config.STS_DATASET_BINARY_EXPLICIT_RS_NAME}.zip", mime="application/zip")
           
def help_contextual_modeling_paradigm():
    with st.expander(label='Help information'):        
        st.markdown(""" In the contextual modeling paradigm, the contextual information is used directly in the modeling technique as part of the estimation of ratings. """)
        st.image(image=config.CM_IMAGE, use_column_width=True, output_format="auto")
        
        st.markdown("""**Example video:**""")
        help_video_from_url(video_url=config.EVALUATION_PREFERENCIAL_CM_CARS_URL, title_video='Evaluation of a CARS (Contextual Modeling paradigm) using preferencial and explicit ratings')
        st.markdown("""**Example datasets:**""")
        st.download_button(label=f"{config.STS_DATASET_PREFERENCIAL_EXPLICIT_CARS_NAME}.zip", data=get_zip_file(config.STS_DATASET_PREFERENCIAL_EXPLICIT_CARS_PATH), file_name=f"{config.STS_DATASET_PREFERENCIAL_EXPLICIT_CARS_NAME}.zip", mime="application/zip")        
        st.download_button(label=f"{config.STS_DATASET_BINARY_EXPLICIT_CARS_NAME}.zip", data=get_zip_file(config.STS_DATASET_BINARY_EXPLICIT_CARS_PATH), file_name=f"{config.STS_DATASET_BINARY_EXPLICIT_CARS_NAME}.zip", mime="application/zip")                

def help_prefiltering_paradigm():
    with st.expander(label='Help information'):
        st.markdown(""" In the pre-filtering paradigm, the contextual information is used to filter the data before applying traditional recommendation algorithms. """)
        st.image(image=config.PREFILTERING_IMAGE, use_column_width=True, output_format="auto")
        
        st.markdown("""**Example video:**""")
        help_video_from_url(video_url=config.EVALUATION_PREFERENCIAL_PREFILTERING_CARS_URL, title_video='Evaluation of a CARS (Pre-Filtering paradigm) using preferencial and explicit ratings')        
        st.markdown("""**Example datasets:**""")
        st.download_button(label=f"{config.STS_DATASET_PREFERENCIAL_EXPLICIT_CARS_NAME}.zip", data=get_zip_file(config.STS_DATASET_PREFERENCIAL_EXPLICIT_CARS_PATH), file_name=f"{config.STS_DATASET_PREFERENCIAL_EXPLICIT_CARS_NAME}.zip", mime="application/zip")        
        st.download_button(label=f"{config.STS_DATASET_BINARY_EXPLICIT_CARS_NAME}.zip", data=get_zip_file(config.STS_DATASET_BINARY_EXPLICIT_CARS_PATH), file_name=f"{config.STS_DATASET_BINARY_EXPLICIT_CARS_NAME}.zip", mime="application/zip")                

def help_postfiltering_paradigm():
    with st.expander(label='Help information'):
        st.markdown(""" In the post-filtering paradigm, the contextual information is considered only in the final step of the process. So, contextual information is initially ignored and the ratings are predicted using any conventional 2D recommendation system, taking all the potential items to recommend into account. Afterwards, the resulting set of recommendations is adjusted (contextualized) for each user by using contextual information. """)
        st.image(image=config.POSTFILTERING_IMAGE, use_column_width=True, output_format="auto")
        
        st.markdown("""**Example video:**""")
        help_video_from_url(video_url=config.EVALUATION_PREFERENCIAL_POSTFILTERING_CARS_URL, title_video='Evaluation of a CARS (Post-Filtering paradigm) using preferencial and explicit ratings')
        st.markdown("""**Example datasets:**""")
        st.download_button(label=f"{config.STS_DATASET_PREFERENCIAL_EXPLICIT_CARS_NAME}.zip", data=get_zip_file(config.STS_DATASET_PREFERENCIAL_EXPLICIT_CARS_PATH), file_name=f"{config.STS_DATASET_PREFERENCIAL_EXPLICIT_CARS_NAME}.zip", mime="application/zip")        
        st.download_button(label=f"{config.STS_DATASET_BINARY_EXPLICIT_CARS_NAME}.zip", data=get_zip_file(config.STS_DATASET_BINARY_EXPLICIT_CARS_PATH), file_name=f"{config.STS_DATASET_BINARY_EXPLICIT_CARS_NAME}.zip", mime="application/zip")                

                                             

def help_classification_algoritms(classifier_name_list):
    with st.expander(label='Help information'): 
        for classifier_name in classifier_name_list:
            if classifier_name == 'KNeighborsClassifier':
                st.markdown("""- ``` KNeighborsClassifier ```: Classifier implementing the k-nearest neighbors vote.""")
            if classifier_name == 'SVC':
                st.markdown("""- ``` SVC ```: C-Support Vector Classification. The implementation is based on libsvm.""")
            if classifier_name == 'GaussianNB':
                st.markdown("""- ``` GaussianNB ```: Gaussian Naive Bayes.""")
            if classifier_name == 'RandomForestClassifier':
                st.markdown("""- ``` RandomForestClassifier ```: A random forest classifier. A random forest is a meta estimator that fits a number of decision tree classifiers on various sub-samples of the dataset and uses averaging to improve the predictive accuracy and control over-fitting.""")
            if classifier_name == 'KMeans':
                st.markdown("""- ``` KMeans ```: K-Means clustering.""")
            if classifier_name == 'HistGradientBoostingClassifier':
                st.markdown("""- ``` HistGradientBoostingClassifier ```: Histogram-based Gradient Boosting Classification Tree. This estimator has native support for missing values (NaNs).""")
        st.markdown("""These algorithms are implemented in the [scikit-learn](https://scikit-learn.org/stable/supervised_learning.html#supervised-learning) python library.""")

####### Videos #######
def help_video_from_file(video_file_path):
    # Display a link to open the video in a new tab    
    video_url = open(video_file_path, "rb").read()
    st.markdown(f'<a href="data:video/mp4;base64,{video_url}" target="_blank">Open Video</a>', unsafe_allow_html=True)

def help_video_from_url(video_url, title_video):
    # Display a link to open the video from URL in a new tab:    
    st.markdown(f'<a href="{video_url}" target="_blank">{title_video}</a>', unsafe_allow_html=True)

####### Datasets #######
def get_zip_file(directory_path):
    """
    Creates an in-memory ZIP file containing all files from the specified directory and its subdirectories.

    Args:
    directory_path (str): The path to the directory whose files are to be zipped.

    Returns:
    BytesIO: An in-memory file-like object containing the ZIP file's data.

    This function navigates through all folders and files in the provided directory path, adds each file into a ZIP file while maintaining their relative paths, and returns a BytesIO object with the complete ZIP file. The ZIP file is created in memory using BytesIO, which avoids the need for temporary storage and results in faster performance and better resource management.
    """
    # Create a buffer to hold the ZIP file in memory
    bytes_io = BytesIO()
    with ZipFile(bytes_io, 'w') as zip_file:
        # Walk through the directory
        for foldername, subfolders, filenames in os.walk(directory_path):
            for filename in filenames:
                # Create the full path to the file
                file_path = os.path.join(foldername, filename)
                # Add file to the ZIP file
                zip_file.write(file_path, arcname=os.path.relpath(file_path, start=directory_path))

    # Move the pointer to the start of the BytesIO buffer
    bytes_io.seek(0)
    return bytes_io
