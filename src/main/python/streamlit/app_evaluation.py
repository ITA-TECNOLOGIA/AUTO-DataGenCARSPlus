import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import altair as alt
import seaborn as sns
from pathlib import Path
import config
sys.path.append("src/main/python")
import rs_surprise.surprise_helpers as surprise_helpers
import rs_surprise.evaluation as evaluation
import datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_rating as extract_statistics_rating
import datagencars.existing_dataset.replicate_dataset.extract_statistics.extract_statistics_uic as extract_statistics_uic
import datagencars.existing_dataset.label_encoding as label_encoding
import datagencars.existing_dataset.mapping_categorization as mapping_categorization
import datagencars.existing_dataset.replicate_dataset.binary_ratings as binary_ratings

# Setting the main page:
st.set_page_config(page_title='AUTO-DataGenCARS',
                   page_icon=config.AUTO_DATAGENCARS_ICON,
                   layout="centered", # "centered", "wide"
                   initial_sidebar_state="auto", # "expanded", "auto", "collapsed"
                   menu_items= None)

# Description, title and icon:
st.markdown("""---""")
col1, col2 = st.columns(2)
with col1:
    # Title:
    st.title('AUTO-DataGenCARS')
    # Description:
    st.write('DataGenCARS is a complete Java-based synthetic dataset generator for the evaluation of Context-Aware Recommendation Systems (CARS) to obtain the required datasets for any type of scenario desired.')
with col2:    
    # Icon:
    st.image(image=config.AUTO_DATAGENCARS_ICON, use_column_width=False, output_format="auto") # width=200, 
st.markdown("""---""")

# Tool bar:
general_option = st.sidebar.selectbox(label='**Options available:**', options=['Select one option', 'Generate a synthetic dataset', 'Analysis an existing dataset', 'Evaluation of a dataset'])

if general_option == 'Generate a synthetic dataset':
    context = None
    if is_context := st.sidebar.checkbox('With context', value=True):        
        context = True
        tab_generation, tab_user, tab_item, tab_context  = st.tabs(['Generation', 'Users', 'Items', 'Contexts'])
    else:
        context = False        
        tab_generation, tab_user, tab_item = st.tabs(['Generation', 'Users', 'Items'])  

    # GENERATION SETTINGS:
    with tab_generation:
        st.header('Generation')
        value = ''
        if is_upload_generation := st.checkbox('Upload generation file', value=True):
            if generation_config_file := st.file_uploader(label='Choose the generation file:', key='generation_config_file'):
                value = generation_config_file.getvalue().decode("utf-8")
        else:
            # [dimension]
            st.write('General configuration')
            dimension_value = '[dimension] \n'
            user_count = st.number_input(label='Number of users to generate:', value=0)
            item_count = st.number_input(label='Number of items to generate:', value=0)
            if context:
                context_count = st.number_input(label='Number of contexts to generate:', value=0)
                dimension_value += ('number_user=' + str(user_count) + '\n' +
                                    'number_item=' + str(item_count) + '\n' +
                                    'number_context=' + str(context_count) + '\n')
            else:            
                dimension_value = ('number_user=' + str(user_count) + '\n' +
                                   'number_item=' + str(item_count) + '\n')
            st.markdown("""---""")
            # [rating]
            st.write('Rating configuration')
            rating_value = '[rating] \n'
            rating_count = st.number_input(label='Number of ratings to generate:', value=0)
            rating_min = st.number_input(label='Minimum value of the ratings:', value=1, key='rating_min')
            rating_max = st.number_input(label='Maximum value of the ratings:', value=5, key='rating_max')
            rating_impact = st.number_input(label='Impact of user expectatiosn in future ratings (%):', value=25)            
            rating_distribution = st.selectbox(label='Choose a distribution to generate the ratings:', options=['Uniform', 'Gaussian'])                        
            # st.write('Dates of the ratings to generate (years only):')
            # rating_min = st.number_input(label='From:', value=1980)
            # rating_max = st.number_input(label='Until:', value=2020)                
            rating_value += ('number_rating=' + str(rating_count) + '\n' +
                             'minimum_value_rating=' + str(rating_min) + '\n' +
                             'maximum_value_rating=' + str(rating_max) + '\n' + 
                             'percentage_rating_variation=' + str(rating_impact) + '\n' +
                             'gaussian_distribution=' + str(rating_distribution) + '\n')
            st.markdown("""---""")
            # [item profile]
            st.write('Item profile configuration')
            item_profile_value = '[item profile] \n'
            probability_percentage_profile_1 = st.number_input(label='Profile probability percentage 1:', value=10)
            probability_percentage_profile_2 = st.number_input(label='Profile probability percentage 2:', value=30)
            probability_percentage_profile_3 = st.number_input(label='Profile probability percentage 3:', value=60)
            noise_percentage_profile_1 = st.number_input(label='Profile noise percentage 1:', value=20)
            noise_percentage_profile_2 = st.number_input(label='Profile noise percentage 2:', value=20)
            noise_percentage_profile_3 = st.number_input(label='Profile noise percentage 3:', value=20)            
            item_profile_value += ('probability_percentage_profile_1=' + str(probability_percentage_profile_1) + '\n' +
                                   'probability_percentage_profile_2=' + str(probability_percentage_profile_2) + '\n' +
                                   'probability_percentage_profile_3=' + str(probability_percentage_profile_3) + '\n' +
                                   'noise_percentage_profile_1=' + str(noise_percentage_profile_1) + '\n' +
                                   'noise_percentage_profile_2=' + str(noise_percentage_profile_2) + '\n' +
                                   'noise_percentage_profile_3=' + str(noise_percentage_profile_3) + '\n')
            value = dimension_value + '\n' + rating_value + '\n' + item_profile_value                         

    # USER SETTINGS:
    with tab_user:        
        st.header('Users')
        schema_type = 'user'
    # ITEM SETTINGS:
    with tab_item:
        st.header('Items')
        schema_type = 'item'
    # CONTEXT SETTINGS:
    if context:
        with tab_context:
            st.header('Contexts')
            schema_type = 'context'

    if is_upload_schema := st.checkbox('Upload schema file', value=True):
        if schema_file := st.file_uploader(label='Choose the schema file:', key='schema_file'):
            value = schema_file.getvalue().decode("utf-8")        
    else:        
        # [global]   
        value = '[global]'+'\n'
        value += 'type='+schema_type+'\n'
        number_attribute = st.number_input(label='Number of attributes to generate:', value=1, key='number_attribute_context')
        value += 'number_attributes='+str(number_attribute)+'\n'
        value += '\n'
        st.markdown("""---""")        

        # [attribute]
        for position in range(1, number_attribute+1):
            value += '[attribute'+str(position)+']'+'\n'
            # name_attribute:     
            attribute_name = st.text_input(label="Attribute's name:", key='attribute_name_'+str(position))
            value += 'name_attribute_'+str(position)+'='+attribute_name+'\n'
            # generator_type_attribute:
            generator_type = st.selectbox(label='Generator type:', options=['Random', 'Fixed', 'URL', 'Address', 'Date', 'BooleanArrayList'],  key='generator_type_'+str(position))
            value += 'generator_type_attribute_'+str(position)+'='+generator_type+'AttributeGenerator'+'\n'
            # type_attribute:
            attribute_type = None
            if generator_type == 'Random':                    
                attribute_type = st.selectbox(label='Attribute type:', options=['Integer', 'String', 'Boolean'], key='attribute_type_'+str(position)+'_'+generator_type)
                if attribute_type == 'Integer':
                    # Integer:
                    integer_min = st.number_input(label='Minimum value of the attribute', value=0, key='integer_min_'+str(position))
                    value += 'minimum_value_attribute_'+str(position)+'='+str(integer_min)+'\n'
                    integer_max = st.number_input(label='Maximum value of the ratings', value=0, key='integer_max_'+str(position))
                    value += 'maximum_value_attribute_'+str(position)+'='+str(integer_max)+'\n'
                elif attribute_type == 'String':
                    # String:
                    area_column, button_column = st.columns(2)
                    with area_column:
                        string_text_area = st.text_area(label='Introduce new values to the list (split by comma):', value='rainy, cloudy, sunny', key='string_text_area_'+str(position))  
                        str_possible_value_list = string_text_area.split(',')
                        number_possible_value = len(str_possible_value_list)
                        for i in range(number_possible_value):
                            value += 'posible_value_'+str(i+1)+'attribute_'+str(position)+'='+str_possible_value_list[i]+'\n'
                        value += 'number_posible_values_attribute_'+str(position)+'='+str(number_possible_value)+'\n'                    
                    with button_column:                        
                        export_button = st.download_button(label='Export list', data=string_text_area, file_name='str_possible_value_list.csv', key='export_button_'+str(position)) 
                        if import_file := st.file_uploader(label='Import list', key='import_file'):                            
                            string_text_area = st.text_area(label='Introduce new values to the list (split by comma):', value=import_file.getvalue().decode("utf-8"), key='import_button_'+str(position))                          
                elif attribute_type == 'Boolean':
                    # Boolean:                 
                    boolean_possible_value_list = ['True', 'False']
                    boolean_text_area = st.text_area(label='Introduce new values to the list (split by comma):', value='True, False', key='boolean_text_area_'+str(position))  
            elif generator_type == 'Fixed':                    
                attribute_type = st.selectbox(label='Attribute type:', options=['Integer', 'String', 'Boolean'], key='attribute_type_'+str(position)+'_'+generator_type)
                fixed_input = st.text_input(label='Imput the fixed value:', key='fixed_input_'+str(position))
                value += 'input_parameter_attribute_'+str(position)+'='+str(fixed_input)+'\n'
            elif generator_type == 'URL':                    
                attribute_type = st.selectbox(label='Attribute type:', options=['AttributeComposite'], key='attribute_type_'+str(position)+'_'+generator_type)
            elif generator_type == 'Address':                    
                attribute_type = st.selectbox(label='Attribute type:', options=['AttributeComposite'], key='attribute_type_'+str(position)+'_'+generator_type)
                address_area_column, address_button_column = st.columns(2)
                with address_area_column:
                    st.write('Add this address')
                    street_address = st.text_input(label='Street:', key='street_address_'+str(position))
                    number_address = st.number_input(label='Number:', value=0, key='number_address_'+str(position))
                    zip_code_address = st.number_input(label='Zip Code:', value=0, key='zip_code_address_'+str(position))
                    latitude_address = st.text_input(label='Latitude:', key='latitude_address_'+str(position))
                    longitude_address = st.text_input(label='Latitude:', key='longitude_address_'+str(position))
                    poi_address = st.text_input(label='Place of Interest (e.g., restaurant):', key='poi_address_'+str(position))                    
                with address_button_column:                                                        
                    if add_button := st.button(label='Add', key='add_button_'+str(position)):
                        address_value = f'{street_address};{number_address};{zip_code_address};{latitude_address};{longitude_address}'
                        address_list = st.text_area(label='Introduce new addresses to the list (split by comma):', value=address_value, key='address_list_'+str(position))                    
                    if search_button := st.button(label='Search', key='search_button_'+str(position)):
                        st.write('TODO')
                    if address_export_button := st.button(label='Export list', key='address_export_button_'+str(position)):
                        st.write('TODO')
                    if address_import_button := st.button(label='Import list', key='address_import_button_'+str(position)):
                        st.write('TODO')
            elif generator_type == 'Date':                    
                attribute_type = st.selectbox(label='Attribute type:', options=['Integer'], key='attribute_type_'+str(position)+'_'+generator_type)
                st.write('Imput the range of dates (years only):')
                date_min = st.number_input(label='From:', value=1980, key='date_min_'+str(position))
                value += 'minimum_value_attribute_'+str(position)+'='+str(date_min)+'\n'
                date_max = st.number_input(label='Until:', value=2020, key='date_max_'+str(position))
                value += 'maximum_value_attribute_'+str(position)+'='+str(date_max)+'\n'
            elif generator_type == 'BooleanArrayList':                    
                attribute_type = st.selectbox(label='Attribute type:', options=['ArrayList'], key='attribute_type_'+str(position)+'_'+generator_type)
                boolean_list = st.text_area(label='Introduce boolean values to the list (split by comma):', value='True, False, True', key='boolean_list_'+str(position))                
            value += 'type_attribute_'+str(position)+'='+attribute_type+'\n'                                                                                                                             
            # distribution_type = st.selectbox(label='Distribution type:', options=['Uniform', 'Gaussian'], key='distribution_type_'+str(position))
            # with_correlation = st.checkbox('Attribute with correlation', value=True)
            value += '\n'
            st.markdown("""---""")  

    if edit_schema := st.checkbox(label='Edit file?'):
        user_schema_text_area = st.text_area(label='Current file:', value=value, height=500)
    else:
        user_schema_text_area = st.text_area(label='Current file:', value=value, height=500, disabled=True)
    st.download_button(label='Download', data=user_schema_text_area, file_name=schema_type+'_schema.conf')  

elif general_option == 'Analysis an existing dataset':
    # TODO: CONTEXT
    is_analysis = st.sidebar.radio(label='Analysis an existing dataset', options=['Data visualization', 'Replicate dataset', 'Extend dataset', 'Recalculate ratings', 'Replace NULL values', 'Generate user profile', 'Ratings to binary', 'Mapping categorization'])
    if is_analysis == 'Data visualization':
        if is_context := st.sidebar.checkbox('With context', value=True):
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Upload dataset', 'Users', 'Items', 'Contexts', 'Ratings', 'Total'])
        else:
            tab1, tab2, tab3, tab5, tab6 = st.tabs(['Upload dataset', 'Users', 'Items', 'Ratings', 'Total'])
        def read_uploaded_file(uploaded_file, data, file_type, separator):
            # Read the header of the file to determine column names
            header = uploaded_file.readline().decode("utf-8").strip()
            column_names = header.split(separator)

            # Rename columns
            for i, col in enumerate(column_names):
                if "user" in col.lower() and "id" in col.lower():
                    column_names[i] = "user_id"
                elif "item" in col.lower() and "id" in col.lower():
                    column_names[i] = "item_id"
                elif "context" in col.lower() and "id" in col.lower():
                    column_names[i] = "context_id"

            data[file_type] = pd.read_csv(uploaded_file, sep=separator, names=column_names)
            return data
        def plot_column_attributes_count(data, column):                    
            chart = alt.Chart(data).mark_bar().encode(
                    x=alt.X(column + ':O', title='Attribute values'),
                    y=alt.Y('count:Q', title='Count'),
                    tooltip=['count']
                ).interactive()
            st.altair_chart(chart, use_container_width=True)
        def print_statistics_by_attribute(statistics):
            st.header("Statistics by attribute")
            for stat in statistics:
                st.subheader(stat[0])
                st.write('Average: ', stat[1])
                st.write('Standard deviation: ', stat[2])
                st.write('Frequencies:')
                st.dataframe(stat[3])
                st.write('Percentages:')
                st.dataframe(stat[4])
        with tab1:
            option = st.selectbox('Choose between uploading multiple files or a single file:', ('Multiple files', 'Single file'))
            if option == 'Multiple files':
                data = {} #Dictionary with the dataframes
                for file_type in ["user", "item", "context", "rating"]:
                    if file_type == "context":
                        if not is_context:
                            continue
                    with st.expander(f"Upload your {file_type}.csv file"):
                        uploaded_file = st.file_uploader(f"Select {file_type}.csv file", type="csv")
                        separator = st.text_input(f"Enter the separator for your {file_type}.csv file (default is ';')", ";")
                        if uploaded_file is not None:
                            if not separator:
                                st.error('Please provide a separator.')
                            else:
                                try:
                                    data = read_uploaded_file(uploaded_file, data, file_type, separator)
                                    st.dataframe(data[file_type].head())
                                except Exception as e:
                                    st.error(f"An error occurred while reading the {file_type} file: {str(e)}")
                                    data[file_type] = None
            elif option == 'Single file':
                data = {} #Dictionary with the dataframes
                data_file = st.file_uploader("Select Data_STS.csv file", type="csv")
                separator = st.text_input("Enter the separator for your Data_STS.csv file (default is '	')", "	")
                if data_file is not None:
                    if not separator:
                        st.error('Please provide a separator.')
                    else:
                        try:
                            df = pd.read_csv(data_file, sep=separator)
                            st.dataframe(df.head())
                            def create_dataframe(label, df):
                                if columns := st.multiselect(label=label, options=df.columns):
                                    # Create a new dataframe with the selected columns
                                    new_df = df[columns]
                                    st.dataframe(new_df.head())
                                    return new_df
                                else:
                                    st.error('Please select at least one column')
                            data = {'user': create_dataframe('Select the columns for the user dataframe:', df, 'user_df'),
                                    'item': create_dataframe('Select the columns for the item dataframe:', df, 'item_df'),
                                    'context': create_dataframe('Select the columns for the context dataframe:', df, 'context_df'),
                                    'rating': create_dataframe('Select the columns for the rating dataframe:', df, 'rating_df')}
                        except Exception as e:
                            st.error(f"An error occurred while reading the file: {str(e)}")
        with tab2:
            if 'user' in data and data['user'] is not None:
                st.dataframe(data['user'] )
                missing_values2 = extract_statistics_uic.count_missing_values(data['user'],replace_values={"NULL":np.nan,-1:np.nan})
                st.write("Missing values:")
                st.table(missing_values2)
                
                st.write("Attributes, data types and value ranges:")
                table2 = extract_statistics_uic.list_attributes_and_ranges(data['user'])
                st.table(pd.DataFrame(table2, columns=["Attribute name", "Data type", "Value ranges"]))
                
                column2 = st.selectbox("Select an attribute", data['user'].columns)
                data2 = extract_statistics_uic.column_attributes_count(data['user'], column2)
                plot_column_attributes_count(data2, column2)

                statistics = extract_statistics_uic.statistics_by_attribute(data['user'])
                print_statistics_by_attribute(statistics)
            else:
                st.error("User dataset not found.")
        with tab3:
            if 'item' in data and data['item'] is not None:
                st.dataframe(data['item'] )
                missing_values3 = extract_statistics_uic.count_missing_values(data['user'],replace_values={"NULL":np.nan,-1:np.nan})
                st.write("Missing values:")
                st.table(missing_values3)
                
                st.write("Attributes, data types and value ranges:")
                table3 = extract_statistics_uic.list_attributes_and_ranges(data['item'])
                st.table(pd.DataFrame(table3, columns=["Attribute name", "Data type", "Value ranges"]))

                column3 = st.selectbox("Select an attribute", data['item'].columns)
                data3 = extract_statistics_uic.column_attributes_count(data['item'], column3)
                plot_column_attributes_count(data3, column3)

                if 'rating' in data and data['rating'] is not None:
                    merged_df = pd.merge(data['rating'], data['item'], on="item_id")
                    users = merged_df['user_id'].unique()
                    selected_user = st.selectbox("Select a user:", users, key="selected_user_tab3")
                    stats = extract_statistics_uic.statistics_by_user(merged_df, selected_user, "items")
                    st.table(pd.DataFrame([stats]))

                statistics = extract_statistics_uic.statistics_by_attribute(data['item'])
                print_statistics_by_attribute(statistics)
            else:
                st.error("Item dataset not found.")
        if is_context:
            with tab4:
                if 'context' in data and data['context'] is not None:
                    st.dataframe(data['context'] )
                    missing_values4 = extract_statistics_uic.count_missing_values(data['user'],replace_values={"NULL":np.nan,-1:np.nan})
                    st.write("Missing values:")
                    st.table(missing_values4)

                    st.write("Attributes, data types and value ranges:")
                    table4 = extract_statistics_uic.list_attributes_and_ranges(data['context'])
                    st.table(pd.DataFrame(table4, columns=["Attribute name", "Data type", "Value ranges"]))
                    
                    column4 = st.selectbox("Select an attribute", data['context'].columns)
                    data4 = extract_statistics_uic.column_attributes_count(data['context'], column4)
                    plot_column_attributes_count(data3, column3)

                    if 'rating' in data and data['rating'] is not None:
                        merged_df = pd.merge(data['rating'], data['context'], on="context_id")
                        users = merged_df['user_id'].unique()
                        selected_user = st.selectbox("Select a user:", users, key="selected_user_tab4")
                        stats = extract_statistics_uic.statistics_by_user(merged_df, selected_user, "contexts")
                        st.table(pd.DataFrame([stats]))

                    statistics = extract_statistics_uic.statistics_by_attribute(data['context'])
                    print_statistics_by_attribute(statistics)
                else:
                    st.error("Context dataset not found.")
        with tab5:
            if 'rating' in data and data['rating'] is not None:
                data['rating'] = extract_statistics_rating.replace_missing_values(data['rating'])
                st.session_state["rating"] = data['rating'] #Save the rating dataframe in the session state

                st.dataframe(data['rating'])

                unique_counts_df = extract_statistics_rating.count_unique(data['rating'])
                st.write("General statistics:")
                st.table(unique_counts_df)
                
                st.write("Attributes, data types and value ranges:")
                table5 = extract_statistics_uic.list_attributes_and_ranges(data['rating'])
                st.table(pd.DataFrame(table5, columns=["Attribute name", "Data type", "Value ranges"]))

                # Plot the distribution of ratings
                counts = np.bincount(data['rating']['rating']) #Count the frequency of each rating
                fig, ax = plt.subplots()
                ax.set_title("Distribution of ratings", fontdict={'size': 16, **config.PLOTS_FONT})
                ax.set_xlabel("Rating", fontdict=config.PLOTS_FONT)
                ax.set_ylabel("Frequency", fontdict=config.PLOTS_FONT)
                ax.grid(**config.PLOTS_GRID)
                ax.set_xticks(range(len(counts)))
                for i in range(len(counts)):
                    if counts[i] > 0:
                        ax.bar(i, counts[i], color="#0099CC")
                        ax.text(i, counts[i], str(counts[i]), ha='center')
                st.pyplot(fig, clear_figure=True)

                # Plot the distribution of the number of items voted by each user
                users = data['rating']['user_id'].unique()
                selected_user = st.selectbox("Select a user:", users, key="selected_user_tab5")
                counts_items, unique_items, total_count, percent_ratings_by_user = extract_statistics_rating.count_items_voted_by_user(data['rating'], selected_user)
                fig, ax = plt.subplots()
                ax.set_title(f"Number of items voted by user {str(selected_user)} (total={total_count}) (percentage={percent_ratings_by_user:.2f}%)", fontdict={'size': 16, **config.PLOTS_FONT})
                ax.set_xlabel("Items", fontdict=config.PLOTS_FONT)
                ax.set_ylabel("Frequency", fontdict=config.PLOTS_FONT)
                ax.grid(**config.PLOTS_GRID)
                ax.bar(counts_items.index, counts_items.values, color="#0099CC")
                ax.set_xticks(unique_items)
                for item, count in counts_items.items(): #Add the count of each item to the plot
                    ax.text(item, count, str(count), ha='center', va='bottom')
                st.pyplot(fig)

                # Show the statistics of the selected user votes
                users = ["All users"] + list(users)
                selected_user = st.selectbox("Select user", users)
                vote_stats = extract_statistics_rating.calculate_vote_stats(data['rating'], selected_user)
                for key, value in vote_stats.items():
                    st.write(f"{key}: {value}")
            else:
                st.error("Ratings dataset not found.")
        with tab6:
            try:
                # Merge the dataframes
                merged_df = data["rating"]
                for key in ["user", "item", "context"]:
                    if key in data:
                        merged_df = pd.merge(merged_df, data[key], on=key+"_id", how="left")

                stats = extract_statistics_uic.general_statistics(merged_df)
                st.table(pd.DataFrame([stats]))
                
                st.header("Correlation matrix")
                columns_not_id = [col for col in merged_df.columns if col not in ['user_id', 'item_id', 'context_id']]
                data_types = []
                for col in columns_not_id:
                    data_types.append({"Attribute": col, "Data Type": str(merged_df[col].dtype), "File Type": "rating" if col in data["rating"].columns else "item" if col in data["item"].columns else "context" if col in data["context"].columns else "user"})
                df_data_types = pd.DataFrame(data_types)
                st.dataframe(df_data_types)
                selected_columns = st.multiselect("Select columns to analyze", columns_not_id)
                method = st.selectbox("Select a method", ['pearson', 'kendall', 'spearman'])
                if st.button("Generate correlation matrix") and selected_columns:
                    with st.spinner("Generating correlation matrix..."):
                        merged_df_selected = merged_df[selected_columns].copy()
                        # Categorize non-numeric columns using label encoding
                        for col in merged_df_selected.select_dtypes(exclude=[np.number]):
                            merged_df_selected[col], _ = merged_df_selected[col].factorize()
                        
                        corr_matrix = merged_df_selected.corr(method=method)
                        
                        fig, ax = plt.subplots(figsize=(10, 10))
                        sns.heatmap(corr_matrix, vmin=-1, vmax=1, center=0, cmap='coolwarm', annot=True, fmt=".2f", ax=ax)
                        st.pyplot(fig)
            except:
                st.error("Ratings, items, contexts or users datasets not found.")
    elif is_analysis == 'Replicate dataset':
        st.write('TODO')
    elif is_analysis == 'Extend dataset':
        st.write('TODO')
    elif is_analysis == 'Recalculate ratings':
        st.write('TODO')
    elif is_analysis == 'Replace NULL values':
        st.write('TODO')
    elif is_analysis == 'Generate user profile':
        st.write('TODO')
    elif is_analysis == 'Ratings to binary':
        st.title("Rating Binarization")
        with st.expander(label='Help information'):
            st.write('This tool allows you to convert ratings to binary values. For example, if you have a dataset with ratings from 1 to 5, you can convert them to 0 and 1, where 0 represents a negative rating and 1 a positive one.')
            st.write('The tool will convert the ratings to binary values using a threshold. For example, if you set the threshold to 3, all ratings equal or greater than 3 will be converted to 1, and all ratings less than 3 will be converted to 0.')
        def ratings_to_binary(df, threshold=3):
            def binary_rating(rating):
                return 1 if rating >= threshold else 0
            df['rating'] = df['rating'].apply(binary_rating)
            return df
        st.write("Upload a CSV file containing ratings to convert them to binary values.")
        uploaded_file = st.file_uploader("Choose a file")
        delimiter = st.text_input("CSV delimiter", ";")

        if uploaded_file is not None:
            df_ratings = pd.read_csv(uploaded_file, delimiter=delimiter)
            min_rating = df_ratings['rating'].min()
            max_rating = df_ratings['rating'].max()
            threshold = st.number_input(f"Binary threshold (range from {min_rating} to {max_rating})", min_value=min_rating, max_value=max_rating, value=3)
            df_binary = ratings_to_binary(df_ratings, threshold)
            st.write("Converted ratings:")
            st.write(df_binary)
            st.download_button(
                label="Download binary ratings CSV",
                data=df_binary.to_csv(index=False),
                file_name=Path(uploaded_file.name).stem + "_binary.csv",
                mime='text/csv'
            )
    elif is_analysis == 'Mapping categorization':
        option = st.radio(options=['From numerical to categorical', 'From categorical to numerical'], label='Select an option')
        if option == 'From numerical to categorical':
            st.title("Category Encoding")
            with st.expander(label='Help information'):
                st.write("This tool allows you to convert numerical values to categorical values. For example, you can convert the numerical values of a rating scale to the corresponding categories of the scale (e.g. 1-2 -> Bad, 3-4 -> Average, 5 -> Good).")
                st.write("To use this tool, you need to upload a CSV file containing the numerical values to convert. Then, you need to specify the mapping for each numerical value. For example, you could to specify the following mappings: numerical values 1, 2, 3, 4 and 5 to categories Bad, Average, Good, Very good and Excellent, respectively.")
                st.write("Objects and datetime values are ignored.")
            st.write("Upload a CSV file containing numerical values to convert them to categorical values.")
            uploaded_file = st.file_uploader("Choose a file")
            delimiter = st.text_input("CSV delimiter", '\t')
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file, delimiter=delimiter)
                include_nan = st.checkbox("Include NaN values")
                date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%m-%d-%Y", "%Y%m%d"]
                time_formats = ["%H:%M:%S", "%H:%M"]
                mappings = {}
                for col in df.columns:
                    if 'id' not in col.lower() and not pd.api.types.is_datetime64_dtype(df[col]) and not pd.api.types.is_object_dtype(df[col]): # Ignore ID, object and datetime columns
                        unique_values = sorted(df[col].unique())
                        st.write(f"Unique values in {col}: {', '.join(map(str, unique_values))}")
                        col_mappings = {}
                        for val in unique_values:
                            if not include_nan and pd.isna(val):
                                col_mappings[val] = np.nan
                                continue
                            else:
                                mapping = st.text_input(f"Mapping for {val}", "", key=f"{col}_{val}")
                                if mapping:
                                    col_mappings[val] = mapping
                                else:
                                    col_mappings[val] = val
                        mappings[col] = col_mappings
                st.markdown("""---""")
                st.write("Mappings:", mappings)
                if st.button("Generate categorized dataframe"):
                    categorized_df = mapping_categorization.apply_mappings(df, mappings)
                    st.header("Categorized dataset:")
                    st.write(categorized_df)
                    st.download_button(
                        label="Download categorized dataset CSV",
                        data=categorized_df.to_csv(index=False),
                        file_name=Path(uploaded_file.name).stem + "_categorized.csv",
                        mime='text/csv'
                    )
        else:
            st.title("Label Encoding")
            with st.expander(label='Help information'):
                st.write("Label encoding is a process of transforming categorical values into numerical values.")
                st.write("For example, you can convert the categorical values of a rating scale to the corresponding numerical values of the scale (e.g. Bad -> 1, Average -> 2, Good -> 3, Very good -> 4, Excellent -> 5).")
                st.write("To use this tool, you need to upload a CSV file containing the categorical values to convert. Then, you need to select the categorical columns to convert.")
            st.write("Upload a CSV file containing categorical values to convert them to numerical values.")
            uploaded_file = st.file_uploader("Choose a file")
            delimiter = st.text_input("CSV delimiter", '\t')
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file, delimiter=delimiter)
                categorical_cols = [col for col in df.select_dtypes(exclude=[np.number]) if 'id' not in col.lower()]
                if categorical_cols:
                    selected_cols = st.multiselect("Select categorical columns to label encode:", categorical_cols)
                    if selected_cols:
                        if st.button("Encode categorical columns"):
                            encoded_df = label_encoding.apply_label_encoder(df, selected_cols)
                            st.header("Encoded dataset:")
                            st.write(encoded_df)
                            st.download_button(
                                label="Download encoded dataset CSV",
                                data=encoded_df.to_csv(index=False),
                                file_name=Path(uploaded_file.name).stem + "_encoded.csv",
                                mime='text/csv'
                            )
                else:
                    st.write("No categorical columns found.")
elif general_option == 'Evaluation of a dataset':
    def select_params(algorithm):
        if algorithm == "SVD":
            return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_svd'),
                    "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_svd'),
                    "lr_all": st.sidebar.number_input("Learning rate for all parameters", min_value=0.0001, max_value=1.00, value=0.005, step=0.0001, key='lr_all_svd'),
                    "reg_all": st.sidebar.number_input("Regularization term for all parameters", min_value=0.0001, max_value=1.00, value=0.02, key='reg_all_svd')}
        elif algorithm == "KNNBasic":
            return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbasic'),
                    "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["cosine", "msd", "pearson"], key='sim_options_knnbasic'),
                                    "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnbasic')}}
        elif algorithm == "BaselineOnly":
            return {"bsl_options": {"method": st.sidebar.selectbox("Baseline method", ["als", "sgd"], key='method_baselineonly'),
                                    "reg_i": st.sidebar.number_input("Regularization term for item parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_i_baselineonly'),
                                    "reg_u": st.sidebar.number_input("Regularization term for user parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_u_baselineonly')}}
        elif algorithm == "CoClustering":
            return {"n_cltr_u": st.sidebar.number_input("Number of clusters for users", min_value=1, max_value=1000, value=5),
                    "n_cltr_i": st.sidebar.number_input("Number of clusters for items", min_value=1, max_value=1000, value=5)}
        elif algorithm == "KNNBaseline":
            return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbaseline'),
                    "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["cosine", "msd", "pearson"], key='sim_options_knnbaseline'),
                                    "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnbaseline')},
                    "bsl_options": {"method": st.sidebar.selectbox("Baseline method", ["als", "sgd"], key='method_knnbaseline'),
                                    "reg_i": st.sidebar.number_input("Regularization term for item parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_i_knnbaseline'),
                                    "reg_u": st.sidebar.number_input("Regularization term for user parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_u_knnbaseline')}}
        elif algorithm == "KNNWithMeans":
            return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnwithmeans'),
                    "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["cosine", "msd", "pearson"], key='sim_options_knnwithmeans'),
                                    "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnwithmeans')}}
        elif algorithm == "NMF":
            return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_nmf'),
                    "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_nmf'),
                    "reg_pu": st.sidebar.number_input("Regularization term for user factors", min_value=0.0001, max_value=1.0, value=0.02),
                    "reg_qi": st.sidebar.number_input("Regularization term for item factors", min_value=0.0001, max_value=1.0, value=0.02)}
        elif algorithm == "NormalPredictor":
            return {}
        elif algorithm == "SlopeOne":
            return {}
        elif algorithm == "SVDpp":
            return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_svdpp'),
                    "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_svdpp'),
                    "lr_all": st.sidebar.number_input("Learning rate for all parameters", min_value=0.0001, max_value=1.0, value=0.005, key='lr_all_svdpp'),
                    "reg_all": st.sidebar.number_input("Regularization term for all parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_all_svdpp')}

    def select_split_strategy(strategy):
        if strategy == "KFold":
            return {"n_splits": st.sidebar.number_input("Number of splits", min_value=2, max_value=10, value=5),
                    "shuffle": st.sidebar.checkbox("Shuffle?")}
        elif strategy == "RepeatedKFold":
            return {"n_splits": st.sidebar.number_input("Number of splits", min_value=2, max_value=10, value=5),
                    "n_repeats": st.sidebar.number_input("Number of repeats", min_value=1, max_value=10, value=1),
                    "shuffle": st.sidebar.checkbox("Shuffle?")}
        elif strategy == "ShuffleSplit":
            return {"n_splits": st.sidebar.number_input("Number of splits", min_value=2, max_value=10, value=5),
                    "test_size": st.sidebar.number_input("Test size", min_value=0.1, max_value=0.9, step=0.1, value=0.2),
                    "random_state": st.sidebar.number_input("Random state", min_value=0, max_value=100, value=42)}
        elif strategy == "LeaveOneOut":
            return {}
        elif strategy == "PredefinedKFold":
            return {"folds_file": st.sidebar.file_uploader("Upload folds file")}
        elif strategy == "train_test_split":
            return {"test_size": st.sidebar.number_input("Test size", min_value=0.1, max_value=0.9, step=0.1, value=0.2),
                    "random_state": st.sidebar.number_input("Random state", min_value=0, max_value=100, value=42)}

    def evaluate_algo(algo_list, strategy_instance, metrics, data):
        results = []
        fold_counter = {} # To count the number of folds for each algorithm
        fold_count = 0
        with st.spinner("Evaluating algorithms..."):
            for algo in algo_list:
                fold_count += 1
                cross_validate_results = evaluation.cross_validate(algo, data, measures=metrics, cv=strategy_instance)
                for i in range(strategy_instance.n_splits):
                    row = {}
                    algo_name = type(algo).__name__
                    row["Algorithm"] = algo_name

                    # Modify the name of the metrics to be more readable
                    for key, value in cross_validate_results.items():
                        if key == "fit_time":
                            row["Time (train)"] = value[i]
                        elif key == "test_time":
                            row["Time (test)"] = value[i]
                        elif key == "test_f1_score":
                            row["F1_Score"] = value[i]
                        elif key == "test_recall":
                            row["Recall"] = value[i]
                        elif key == "test_precision":
                            row["Precision"] = value[i]
                        elif key == "test_auc_roc":
                            row["AUC-ROC"] = value[i]
                        else:
                            row[key.replace("test_", "").upper()] = value[i]
                        
                    if algo_name in fold_counter:
                        fold_counter[algo_name] += 1
                    else:
                        fold_counter[algo_name] = 1
                    row["Fold"] = fold_counter[algo_name]

                    results.append(row)
        df = pd.DataFrame(results)
        cols = ["Fold"] + [col for col in df.columns if col != "Fold"] # Move the "Fold" column to the first position
        df = df[cols]
        return df

    def visualize_results_algo(df, algorithm):
        # Filter the dataframe for the chosen algorithm
        filtered_df = df[df["Algorithm"] == algorithm]

        # Create the line chart
        fig = go.Figure()
        for metric in [col for col in df.columns if col not in ["Algorithm", "Fold", "Time (train)", "Time (test)"]]:
            # Create a trace for the current metric
            fig.add_trace(go.Scatter(
                x=filtered_df["Fold"],
                y=filtered_df[metric],
                name=metric
            ))

        fig.update_layout(
            xaxis_title="Fold",
            yaxis_title="Value",
            legend=dict(title="Metrics")
        )
        st.plotly_chart(fig, use_container_width=True)

    def visualize_results_metric(df, metric):
        algorithms = df["Algorithm"].unique()
        fig = go.Figure()
        for algorithm in algorithms:
            # Filter the dataframe for the current algorithm
            filtered_df = df[df["Algorithm"] == algorithm]

            # Create the line chart for the current metric
            fig.add_trace(go.Scatter(
                x=filtered_df["Fold"],
                y=filtered_df[metric],
                name=algorithm
            ))

        fig.update_layout(
            xaxis_title="Fold",
            yaxis_title="Value",
            legend=dict(title="Algorithms")
        )
        st.plotly_chart(fig, use_container_width=True)

    st.sidebar.title('Evaluation of a dataset')
    st.sidebar.header("Algorithm selection")
    algorithms = st.sidebar.multiselect("Select one or more algorithms", ["BaselineOnly", "CoClustering", "KNNBaseline", "KNNBasic", "KNNWithMeans", "NMF", "NormalPredictor", "SlopeOne", "SVD", "SVDpp"], default="SVD")
    algo_list = []
    for algorithm in algorithms:
        algo_params = select_params(algorithm)
        algo_instance = surprise_helpers.create_algorithm(algorithm, algo_params)
        algo_list.append(algo_instance)
        st.sidebar.markdown("""---""")
    
    st.sidebar.header("Split strategy selection")
    strategy = st.sidebar.selectbox("Select a strategy", ["KFold", "RepeatedKFold", "ShuffleSplit", "LeaveOneOut", "PredefinedKFold", "train_test_split"])
    strategy_params = select_split_strategy(strategy)
    strategy_instance = surprise_helpers.create_split_strategy(strategy, strategy_params)
    
    if "rating" in st.session_state:
        rating = st.session_state["rating"]
        data = surprise_helpers.convert_to_surprise_dataset(rating)
    else:
        st.error("No rating dataset loaded")

    st.sidebar.header("Metrics selection")
    if binary_ratings.is_binary_rating(rating):
        metrics = st.sidebar.multiselect("Select one or more cross validation binary metrics", ["Precision", "Recall", "F1_Score", "AUC_ROC"], default="Precision")
    else:
        metrics = st.sidebar.multiselect("Select one or more cross validation non-binary metrics", ["RMSE", "MSE", "MAE", "FCP", "Precision", "Recall", "F1_Score", "MAP", "NDCG"], default="MAE")

    if st.sidebar.button("Evaluate"):
        results_df = evaluate_algo(algo_list, strategy_instance, metrics, data)
        st.subheader("Evaluation Results:")
        st.write(pd.DataFrame(results_df))
    #     # results_df.to_csv("results.csv", index=False)    
    #     st.session_state["results"] = results_df #Save the results dataframe in the session state

    # if "results" in st.session_state:
    #     results_df = st.session_state["rating"]
    # results_df = pd.read_csv("results.csv")
    # st.subheader("Algorithm evaluation results")
    # algorithm = st.selectbox("Select an algorithm to plot", algorithms)
    # visualize_results_algo(results_df, algorithm)
    # st.subheader("Metric evaluation results")
    # metric = st.selectbox("Select a metric to plot", metrics)
    # visualize_results_metric(results_df, metric)