# import streamlit as st


# feedback_option_radio = st.sidebar.radio(label='Select a type of user feedback:', options=['Explicit ratings', 'Implicit ratings'])
# if feedback_option_radio == 'Implicit ratings':
#     behavior_df = util.load_one_file('behavior')
# st.header('Visualization')
# if with_context:
#     if feedback_option_radio == 'Implicit ratings':
#         user_tab, item_tab, context_tab, behavior_tab, rating_tab = st.tabs(['Users', 'Items', 'Contexts', 'Behaviors', 'Ratings'])
#     else:
#         user_tab, item_tab, context_tab, rating_tab = st.tabs(['Users', 'Items', 'Contexts', 'Ratings'])
# else:
#     user_tab, item_tab, rating_tab = st.tabs(['Users', 'Items', 'Ratings'])   
# # Users tab:
# with user_tab:
#     if not user_df.empty:
#         try:
#             # User dataframe:
#             st.header("User file")
#             st.dataframe(user_df)
#             # Extracted statistics:
#             extract_statistics_user = ExtractStatisticsUIC(user_df)
#             # Missing values:
#             st.header("Missing values")
#             missing_values2 = extract_statistics_user.count_missing_values(replace_values={"NULL":np.nan,-1:np.nan})                    
#             st.table(missing_values2)
#             # Attributes, data types and value ranges:
#             st.header("Attributes, data types and value ranges")
#             table2 = extract_statistics_user.get_attributes_and_ranges()
#             st.table(pd.DataFrame(table2, columns=["Attribute name", "Data type", "Value ranges"]))
#             # Showing one figure by attribute:
#             st.header("Analysis by attribute")
#             user_attribute_list = user_df.columns.tolist()
#             user_attribute_list.remove('user_id')
#             if len(user_attribute_list) > 0:
#                 col1, col2 = st.columns(2)
#                 with col1:

#                     column2 = st.selectbox("Select an attribute", user_attribute_list, key='column2')
#                 with col2:
#                     sort2 = st.selectbox('Sort', ['none', 'asc', 'desc'], key='sort2')
#                 data2 = extract_statistics_user.column_attributes_count(column2)
#                 util.plot_column_attributes_count(data2, column2, sort2)
#             else:
#                 st.warning(f"No columns (without user_id) to show.")

#             # Showing extracted statistics:
#             st.header("Extracted statistics")                    
#             st.write('Number total of users: ', extract_statistics_user.get_number_id())
#             st.write('Analyzing possible values per attribute:')
#             if len(user_attribute_list) > 0:
#                 number_possible_values_df = extract_statistics_user.get_number_possible_values_by_attribute()
#                 avg_possible_values_df = extract_statistics_user.get_avg_possible_values_by_attribute()
#                 sd_possible_values_df = extract_statistics_user.get_sd_possible_values_by_attribute()                                        
#                 extracted_statistics_df = pd.concat([number_possible_values_df, avg_possible_values_df, sd_possible_values_df])                    
#                 # Insert the new column at index 0:
#                 label_column_list = ['count', 'average', 'standard deviation']                    
#                 extracted_statistics_df.insert(loc=0, column='possible values', value=label_column_list)                  
#                 if extracted_statistics_df.isnull().values.any():
#                     st.warning('If there are <NA> values, it is because these attributes have Nan or string values.')
#                 st.dataframe(extracted_statistics_df)                    
#                 # Showing more details:
#                 with st.expander('More details'):
#                     statistics = extract_statistics_user.statistics_by_attribute()
#                     util.print_statistics_by_attribute(statistics)
#             else:
#                 st.warning(f"No columns (without user_id) to show.")
#             # Showing correlation between attributes:
#             st.header("Correlation between attributes")
#             if len(user_attribute_list) > 1:
#                 corr_matrix = util.correlation_matrix(df=user_df, label='user')                    
#                 if not corr_matrix.empty:                        
#                     fig, ax = plt.subplots(figsize=(10, 10))                    
#                     sns.heatmap(corr_matrix, vmin=-1, vmax=1, center=0, cmap='coolwarm', annot=True, fmt=".2f", ax=ax)
#                     st.pyplot(fig)
#             else:
#                 st.warning(f"At least two columns needed to show correlation.")
#         except Exception as e:
#             st.error(f"Make sure the user dataset is in the right format. {e}")
#     else:
#         st.warning("The user file (user.csv) has not been uploaded.")
# # Items tab:
# with item_tab:
#     if not item_df.empty:
#         try:
#             # Item dataframe:
#             st.header("Item file")
#             st.dataframe(item_df)
#             # Extracted statistics:
#             extract_statistics_item = ExtractStatisticsUIC(item_df)
#             # Missing values:
#             st.header("Missing values")
#             missing_values3 = extract_statistics_item.count_missing_values(replace_values={"NULL":np.nan,-1:np.nan})                    
#             st.table(missing_values3)                    
#             # Attributes, data types and value ranges:
#             st.header("Attributes, data types and value ranges")
#             table3 = extract_statistics_item.get_attributes_and_ranges()
#             st.table(pd.DataFrame(table3, columns=["Attribute name", "Data type", "Value ranges"]))
#             # Showing one figure by attribute:
#             st.header("Analysis by attribute")
#             item_attribute_list = item_df.columns.tolist()
#             item_attribute_list.remove('item_id')
#             if len(item_attribute_list) > 0:
#                 col1, col2 = st.columns(2)
#                 with col1:                        
#                     column3 = st.selectbox("Select an attribute", item_attribute_list, key='column3')
#                 with col2:
#                     sort3 = st.selectbox('Sort', ['none', 'asc', 'desc'], key='sort3')
#                 data3 = extract_statistics_item.column_attributes_count(column3)
#                 util.plot_column_attributes_count(data3, column3, sort3)
#             else:
#                 st.warning(f"No columns (without item_id) to show.")
#             # Showing extracted statistics:
#             st.header("Extracted statistics")
#             st.write('Number total of items: ', extract_statistics_item.get_number_id())
#             st.write('Analyzing possible values per attribute:')
#             if len(item_attribute_list) > 0:
#                 number_possible_values_df = extract_statistics_item.get_number_possible_values_by_attribute()
#                 avg_possible_values_df = extract_statistics_item.get_avg_possible_values_by_attribute()
#                 sd_possible_values_df = extract_statistics_item.get_sd_possible_values_by_attribute()                                        
#                 extracted_statistics_df = pd.concat([number_possible_values_df, avg_possible_values_df, sd_possible_values_df])                    
#                 # Insert the new column at index 0:
#                 label_column_list = ['count', 'average', 'standard deviation']                    
#                 extracted_statistics_df.insert(loc=0, column='possible values', value=label_column_list)                  
#                 if extracted_statistics_df.isnull().values.any():
#                     st.warning('If there are <NA> values, it is because these attributes have Nan or string values.')
#                 st.dataframe(extracted_statistics_df)
#                 # Showing more details:
#                 with st.expander('More details'):                        
#                     statistics = extract_statistics_item.statistics_by_attribute()
#                     util.print_statistics_by_attribute(statistics)
#             else:
#                 st.warning(f"No columns (without item_id) to show.")
#             # Showing correlation between attributes:
#             st.header("Correlation between attributes")
#             if len(item_attribute_list) > 1:
#                 corr_matrix = util.correlation_matrix(df=item_df, label='item')
#                 if not corr_matrix.empty:                        
#                     fig, ax = plt.subplots(figsize=(10, 10))                    
#                     sns.heatmap(corr_matrix, vmin=-1, vmax=1, center=0, cmap='coolwarm', annot=True, fmt=".2f", ax=ax)
#                     st.pyplot(fig)
#             else:
#                 st.warning(f"At least two columns needed to show correlation.")
#         except Exception as e:
#             st.error(f"Make sure the item dataset is in the right format. {e}")
#     else:
#         st.warning("The item file (item.csv) has not been uploaded.")
# # Contexts tab:
# if with_context:
#     with context_tab:
#         if not context_df.empty:
#             try:
#                 # Context dataframe:
#                 st.header("Context file")
#                 st.dataframe(context_df)
#                 # Extracted statistics:
#                 extract_statistics_context = ExtractStatisticsUIC(context_df)
#                 # Missing values:
#                 st.header("Missing values")
#                 missing_values4 = extract_statistics_context.count_missing_values(replace_values={"NULL":np.nan,-1:np.nan})                        
#                 st.table(missing_values4)
#                 # Attributes, data types and value ranges:
#                 st.header("Attributes, data types and value ranges")
#                 table4 = extract_statistics_context.get_attributes_and_ranges()
#                 st.table(pd.DataFrame(table4, columns=["Attribute name", "Data type", "Value ranges"]))
#                 # Showing one figure by attribute:
#                 st.header("Analysis by attribute")
#                 context_attribute_list = context_df.columns.tolist()
#                 context_attribute_list.remove('context_id')
#                 if len(context_attribute_list) > 0:
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         column4 = st.selectbox("Select an attribute", context_attribute_list, key='column4')
#                     with col2:
#                         sort4 = st.selectbox('Sort', ['none', 'asc', 'desc'], key='sort4')
#                     data4 = extract_statistics_context.column_attributes_count(column4)
#                     util.plot_column_attributes_count(data4, column4, sort4)
#                 else:
#                     st.warning(f"No columns (without context_id) to show.")
#                 # Showing extracted statistics:
#                 st.header("Extracted statistics")
#                 st.write('Number total of contexts: ', extract_statistics_context.get_number_id())
#                 st.write('Analyzing possible values per attribute:')
#                 if len(context_attribute_list) > 0:
#                     number_possible_values_df = extract_statistics_context.get_number_possible_values_by_attribute()
#                     avg_possible_values_df = extract_statistics_context.get_avg_possible_values_by_attribute()
#                     sd_possible_values_df = extract_statistics_context.get_sd_possible_values_by_attribute()                                        
#                     extracted_statistics_df = pd.concat([number_possible_values_df, avg_possible_values_df, sd_possible_values_df])                    
#                     # Insert the new column at index 0:
#                     label_column_list = ['count', 'average', 'standard deviation']                    
#                     extracted_statistics_df.insert(loc=0, column='possible values', value=label_column_list)                  
#                     if extracted_statistics_df.isnull().values.any():
#                         st.warning('If there are <NA> values, it is because these attributes have Nan or string values.')
#                     st.dataframe(extracted_statistics_df)
#                     # Showing more details:
#                     with st.expander('More details'):
#                         statistics = extract_statistics_context.statistics_by_attribute()
#                         util.print_statistics_by_attribute(statistics)
#                 else:
#                     st.warning(f"No columns (without context_id) to show.")
#                 # Showing correlation between attributes:
#                 st.header("Correlation between attributes")
#                 if len(context_attribute_list) > 1:
#                     corr_matrix = util.correlation_matrix(df=context_df, label='context')
#                     if not corr_matrix.empty:                        
#                         fig, ax = plt.subplots(figsize=(10, 10))                    
#                         sns.heatmap(corr_matrix, vmin=-1, vmax=1, center=0, cmap='coolwarm', annot=True, fmt=".2f", ax=ax)
#                         st.pyplot(fig)
#                 else:
#                     st.warning(f"At least two columns needed to show correlation.")
#             except Exception as e:
#                 st.error(f"Make sure the context dataset is in the right format. {e}")
#         else:
#             st.warning("The context file (context.csv) has not been uploaded.")
# # Behaviors tab:
# if with_context and feedback_option_radio == 'Implicit ratings':
#     with behavior_tab:
#         if not behavior_df.empty:
#             # Behavior dataframe:
#             st.header("Behavior file")          
#             st.dataframe(behavior_df)
#             # Extracted statistics:
#             extract_statistics_behavior = ExtractStatisticsUIC(behavior_df)
#             # Missing values:
#             st.header("Missing values")
#             missing_values5 = extract_statistics_behavior.count_missing_values(replace_values={"NULL":np.nan,-1:np.nan})
#             st.table(missing_values5)
#             # Attributes, data types and value ranges:
#             st.header("Attributes, data types and value ranges")
#             table5 = extract_statistics_behavior.get_attributes_and_ranges()
#             st.table(pd.DataFrame(table5, columns=["Attribute name", "Data type", "Value ranges"]))
#             # Showing one figure by attribute:
#             st.header("Analysis by attribute")
#             behavior_attribute_list = behavior_df.columns.tolist()
#             behavior_attribute_list.remove('user_id')
#             if len(behavior_attribute_list) > 0:
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     column5 = st.selectbox("Select an attribute", behavior_attribute_list, key='column5')
#                 with col2:
#                     sort5 = st.selectbox('Sort', ['none', 'asc', 'desc'], key='sort5')
#                 data5 = extract_statistics_behavior.column_attributes_count(column5)
#                 util.plot_column_attributes_count(data5, column5, sort5)
#             else:
#                 st.warning(f"No columns (without user_id) to show.")
#             if not item_df.empty:
#                 try:
#                     # Create a dictionary of colors and assign a unique color to each object_type
#                     unique_object_types = item_df['object_type'].unique()
#                     colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_object_types)))
#                     color_map = {object_type: color for object_type, color in zip(unique_object_types, colors)}

#                     behavior_df['item_id'] = behavior_df['item_id'].astype(str)
#                     item_df['item_id'] = item_df['item_id'].astype(str)
#                     data = pd.merge(behavior_df, item_df, left_on='item_id', right_on='item_id', how='left')
#                     update_data = data[data['object_action'] == 'Update']

#                     # Extract positions and convert them to a list of tuples
#                     update_data['user_position'] = update_data['user_position'].apply(lambda x: literal_eval(x) if x else None)
#                     update_data = update_data.dropna(subset=['user_position'])
#                     unique_user_ids = update_data['user_id'].unique()

#                     st.header('Virtual World Map')
#                     rooms_input = st.text_input('Introduce rooms as list of dictionaries:')
#                     if rooms_input:
#                         try:
#                             rooms = literal_eval(rooms_input)
#                             room_ids = [room['id'] for room in rooms]
#                             selected_rooms = st.multiselect('Select rooms to plot:', options=room_ids)
#                             selected_users = st.multiselect('Select users to plot:', options=unique_user_ids)
#                             selected_data = st.selectbox('Select data to plot:', options=['Items and Users', 'Only Items', 'Only Users', ])

#                             if st.button('Show Map'):
#                                 plt.figure(figsize=(10, 10))

#                                 # Draw the object_types and save the references for the legend
#                                 markers = []
#                                 labels = []
#                                 for user_id in selected_users:
#                                     user_data = update_data[update_data['user_id'] == user_id]

#                                     # Convert the 'timestamp' column to a numeric Unix timestamp
#                                     user_data['timestamp'] = pd.to_datetime(user_data['timestamp'])
#                                     user_data['timestamp'] = user_data['timestamp'].apply(lambda x: pd.Timestamp(x).timestamp())

#                                     # Group the data by session
#                                     sessions = defaultdict(list)
#                                     for _, row in user_data.iterrows():
#                                         user_id = row['user_id']
#                                         timestamp = row['timestamp']
#                                         session_id = np.argmin([abs(r['timestamp'] - timestamp) for _, r in user_data.iterrows() if r['user_id'] == user_id])
#                                         session_timestamp = np.mean([r['timestamp'] for _, r in user_data.iterrows() if r['user_id'] == user_id and np.argmin([abs(r2['timestamp'] - r['timestamp']) for _, r2 in user_data.iterrows() if r2['user_id'] == user_id]) == session_id])
#                                         sessions[(user_id, session_timestamp)].append(row.to_dict())

#                                     for (user_id, session_timestamp), session_data in sessions.items():
#                                         if len(session_data) > 1:
#                                             for room in rooms:
#                                                 if room['id'] in selected_rooms:
#                                                     plt.gca().add_patch(plt.Rectangle((room['x_min'], room['z_min']), room['x_max'] - room['x_min'], room['z_max'] - room['z_min'], fill=None, edgecolor='black', linestyle='--'))
#                                                     plt.text(room['x_min'] + (room['x_max'] - room['x_min']) / 2, room['z_min'] + (room['z_max'] - room['z_min']) / 2, f"ID: {room['id']}", fontsize=12, ha='center', va='center')

#                                             if selected_data in ['Only Items', 'Items and Users']:
#                                                 for index, row in item_df.iterrows():
#                                                     pos = literal_eval(row['object_position'])
#                                                     marker = plt.scatter(pos[0], pos[2], marker='s', color=color_map[row['object_type']])
                                                    
#                                                     if row['object_type'] not in labels:
#                                                         markers.append(marker)
#                                                         labels.append(row['object_type'])

#                                             if selected_data in ['Only Users', 'Items and Users']:
#                                                 positions = [d['user_position'] for d in session_data]
#                                                 timestamps = [d['timestamp'] for d in session_data]
#                                                 x_coords = list(pos[0] for pos in positions)
#                                                 z_coords = list(pos[2] for pos in positions)
#                                                 plt.plot(x_coords, z_coords, label=f'User {user_id}, Session {session_timestamp}', linestyle='--', marker='o')

#                                                 # Print the timestamps for the session
#                                                 st.write(f"Timestamps for User {user_id}, Session {session_timestamp}:")
#                                                 for i, time in enumerate(timestamps):
#                                                     st.write(f"Step {i+1}: {time}")

#                                 plt.title("Virtual world map")
#                                 plt.xlabel('X')
#                                 plt.ylabel('Z')

#                                 # Adjust the limits of the graph according to the selected rooms
#                                 x_mins, x_maxs = zip(*[(room['x_min'], room['x_max']) for room in rooms if room['id'] in selected_rooms])
#                                 z_mins, z_maxs = zip(*[(room['z_min'], room['z_max']) for room in rooms if room['id'] in selected_rooms])
#                                 plt.xlim(min(x_mins), max(x_maxs))
#                                 plt.ylim(min(z_mins), max(z_maxs))

#                                 plt.legend(handles=markers+plt.gca().get_legend_handles_labels()[0], labels=labels+plt.gca().get_legend_handles_labels()[1])
#                                 plt.grid(True)
#                                 st.pyplot(plt.gcf())
#                                 plt.clf()
#                         except Exception as e:
#                             st.error(f"Error parsing the rooms: {e}. Make sure the format is correct.")
#                 except Exception as e:
#                     st.error(f"Make sure the behavior dataset is in the right format. {e}")
# # Ratings tab:
# with rating_tab:
#     if not rating_df.empty:
#         try:
#             # Rating dataframe:
#             st.header("Rating file")          
#             st.dataframe(rating_df)
#             # Extracted statistics:
#             extract_statistics_rating = ExtractStatisticsRating(rating_df=rating_df)                    
#             # General statistics:
#             st.header("General statistics")
#             unique_users = extract_statistics_rating.get_number_users()
#             unique_items = extract_statistics_rating.get_number_items()
#             unique_counts = {"Users": unique_users, "Items": unique_items}
#             if with_context:
#                 unique_contexts = extract_statistics_rating.get_number_contexts()
#                 unique_counts["Contexts"] = unique_contexts
#             unique_ratings = extract_statistics_rating.get_number_ratings()
#             unique_counts["Ratings"] = unique_ratings
#             unique_counts_df = pd.DataFrame.from_dict(unique_counts, orient='index', columns=['Count'])
#             unique_counts_df.reset_index(inplace=True)
#             unique_counts_df.rename(columns={"index": "Attribute name"}, inplace=True)                    
#             st.table(unique_counts_df)               
#             # Attributes, data types and value ranges:
#             st.header("Attributes, data types and value ranges")
#             table6 = extract_statistics_rating.get_attributes_and_ranges()
#             st.table(pd.DataFrame(table6, columns=["Attribute name", "Data type", "Value ranges"]))
#             # Histogram of ratings:
#             st.header("Histogram of ratings")
#             counts = np.bincount(rating_df['rating'])[np.nonzero(np.bincount(rating_df['rating']))] #Count the frequency of each rating
#             df6 = pd.DataFrame({'Type of ratings': np.arange(1, len(counts) + 1), 'Number of ratings': counts})
#             chart6 = alt.Chart(df6).mark_bar(color='#0099CC').encode(
#                 x=alt.X('Type of ratings:O', axis=alt.Axis(title='Type of ratings')),
#                 y=alt.Y('Number of ratings:Q', axis=alt.Axis(title='Number of ratings')),
#                 tooltip=['Type of ratings', 'Number of ratings']
#             ).properties(
#                 title={
#                     'text': 'Histogram of ratings',
#                     'fontSize': 16,
#                 }
#             )                    
#             st.altair_chart(chart6, use_container_width=True)
#             # Statistics per user:
#             st.header("Statistics per user")
#             users = list(rating_df['user_id'].unique())                    
#             selected_user = st.selectbox("Select a user:", users, key="selected_user_tab6")   
#             # Items per user:
#             st.markdown("*Items*")                           
#             counts_items, unique_items, total_count = extract_statistics_rating.get_number_items_from_user(selected_user)
#             df = pd.DataFrame({'Type of items': counts_items.index, 'Number of items': counts_items.values})                    
#             counts_items = pd.Series(counts_items, name='Number of items').reset_index()
#             counts_items = counts_items.rename(columns={'index': 'Type of items'})
#             chart = alt.Chart(counts_items).mark_bar(color="#0099CC").encode(
#                 x=alt.X('Type of items:O', axis=alt.Axis(labelExpr='datum.value', title='Type of items')),
#                 y=alt.Y('Number of items:Q', axis=alt.Axis(title='Number of items')),
#                 tooltip=['Type of items', 'Number of items']
#             ).properties(
#                 title={
#                 "text": [f"Histogram of items rated per user {str(selected_user)} (total={total_count})"],
#                 "fontSize": 16,
#                 }
#             )                    
#             st.altair_chart(chart, use_container_width=True) 
#             # Statistics of items:
#             item_statistics_dict = {}         
#             # Number of items by user:           
#             number_items_df = extract_statistics_rating.get_number_ratings_by_user()
#             number_items = number_items_df.loc[number_items_df['user_id'] == selected_user, 'count_ratings'].iloc[0]
#             # Percentage of items by user:
#             percentage_items_df = extract_statistics_rating.get_percentage_ratings_by_user()                    
#             percentage_items = percentage_items_df.loc[percentage_items_df['user_id'] == selected_user, 'percentage_ratings'].iloc[0]
#             # Average of items by user:    
#             avg_items_df = extract_statistics_rating.get_avg_items_by_user()
#             avg_items = avg_items_df.loc[avg_items_df['user_id'] == selected_user, 'avg_items'].iloc[0]
#             # Variance of items by user:
#             variance_items_df = extract_statistics_rating.get_variance_items_by_user()
#             variance_items = variance_items_df.loc[variance_items_df['user_id'] == selected_user, 'variance_items'].iloc[0]                    
#             # Standard deviation of items by user:
#             sd_items_df = extract_statistics_rating.get_sd_items_by_user()                    
#             sd_items = sd_items_df.loc[sd_items_df['user_id'] == selected_user, 'sd_items'].iloc[0]                    
#             # Number of not repeated items by user:                    
#             number_not_repeated_items_df = extract_statistics_rating.get_number_not_repeated_items_by_user()
#             number_not_repeated_items = number_not_repeated_items_df.loc[number_not_repeated_items_df['user_id'] == selected_user, 'not_repeated_items'].iloc[0]
#             # Percentage of not repeated items by user:                    
#             percentage_not_repeated_items_df = extract_statistics_rating.get_percentage_not_repeated_items_by_user()
#             percentage_not_repeated_items = percentage_not_repeated_items_df.loc[percentage_not_repeated_items_df['user_id'] == selected_user, 'percentage_not_repeated_items'].iloc[0]
#             # Percentage of not repeated items by user:                    
#             percentage_repeated_items_df = extract_statistics_rating.get_percentage_repeated_items_by_user()
#             percentage_repeated_items = percentage_repeated_items_df.loc[percentage_repeated_items_df['user_id'] == selected_user, 'porcentage_repeated_items'].iloc[0]
#             item_statistics_dict['user_id'] = [selected_user]
#             item_statistics_dict['count'] = [number_items]
#             item_statistics_dict['percentage'] = [percentage_items]
#             item_statistics_dict['average'] = [avg_items]                  
#             item_statistics_dict['variance'] = [variance_items]                  
#             item_statistics_dict['standard deviation'] = [sd_items]      
#             item_statistics_dict['not repeated items'] = [number_not_repeated_items]
#             item_statistics_dict['percentage not repeated items'] = [percentage_not_repeated_items]
#             item_statistics_dict['percentage repeated items'] = [percentage_repeated_items]
#             item_statistics_df = pd.DataFrame(item_statistics_dict)
#             st.dataframe(item_statistics_df)   
#             if with_context:
#                 # Contexts per user:                    
#                 st.markdown("*Contexts*")
#                 # Statistics of contexts:
#                 context_statistics_dict = {}         
#                 # Number of contexts by user:           
#                 number_contexts_df = extract_statistics_rating.get_number_ratings_by_user()
#                 number_contexts = number_contexts_df.loc[number_contexts_df['user_id'] == selected_user, 'count_ratings'].iloc[0]
#                 # Percentage of contexts by user:
#                 percentage_contexts_df = extract_statistics_rating.get_percentage_ratings_by_user()
#                 percentage_contexts = percentage_contexts_df.loc[percentage_contexts_df['user_id'] == selected_user, 'percentage_ratings'].iloc[0]
#                 # Average of contexts by user:    
#                 avg_contexts_df = extract_statistics_rating.get_avg_contexts_by_user()
#                 avg_contexts = avg_contexts_df.loc[avg_contexts_df['user_id'] == selected_user, 'avg_contexts'].iloc[0]
#                 # Variance of contexts by user:
#                 variance_contexts_df = extract_statistics_rating.get_variance_contexts_by_user()
#                 variance_contexts = variance_contexts_df.loc[variance_contexts_df['user_id'] == selected_user, 'variance_contexts'].iloc[0]
#                 # Standard deviation of contexts by user:
#                 sd_contexts_df = extract_statistics_rating.get_sd_contexts_by_user()                    
#                 sd_contexts = sd_contexts_df.loc[sd_contexts_df['user_id'] == selected_user, 'sd_contexts'].iloc[0]                    
#                 # Number of not repeated contexts by user:                    
#                 number_not_repeated_contexts_df = extract_statistics_rating.get_number_not_repeated_contexts_by_user()
#                 number_not_repeated_contexts = number_not_repeated_contexts_df.loc[number_not_repeated_contexts_df['user_id'] == selected_user, 'not_repeated_contexts'].iloc[0]
#                 # Percentage of not repeated contexts by user:                    
#                 percentage_not_repeated_contexts_df = extract_statistics_rating.get_percentage_not_repeated_contexts_by_user()
#                 percentage_not_repeated_contexts = percentage_not_repeated_contexts_df.loc[percentage_not_repeated_contexts_df['user_id'] == selected_user, 'percentage_not_repeated_contexts'].iloc[0]
#                 # Percentage of not repeated contexts by user:                    
#                 percentage_repeated_contexts_df = extract_statistics_rating.get_percentage_repeated_contexts_by_user()
#                 percentage_repeated_contexts = percentage_repeated_contexts_df.loc[percentage_repeated_contexts_df['user_id'] == selected_user, 'porcentage_repeated_contexts'].iloc[0]
#                 context_statistics_dict['user_id'] = [selected_user]
#                 context_statistics_dict['count'] = [number_contexts]
#                 context_statistics_dict['percentage'] = [percentage_contexts]
#                 context_statistics_dict['average'] = [avg_contexts]                  
#                 context_statistics_dict['variance'] = [variance_contexts]                  
#                 context_statistics_dict['standard deviation'] = [sd_contexts] 
#                 context_statistics_dict['not repeated contexts'] = [number_not_repeated_contexts]
#                 context_statistics_dict['percentage not repeated contexts'] = [percentage_not_repeated_contexts]
#                 context_statistics_dict['percentage repeated contexts'] = [percentage_repeated_contexts]     
#                 context_statistics_df = pd.DataFrame(context_statistics_dict)
#                 st.dataframe(context_statistics_df)    
#             # Ratings per user:                    
#             st.markdown("*Ratings*")                  
#             rating_statistics_dict = {}         
#             # Number of ratings by user:           
#             number_ratings_df = extract_statistics_rating.get_number_ratings_by_user()
#             number_ratings = number_ratings_df.loc[number_ratings_df['user_id'] == selected_user, 'count_ratings'].iloc[0]
#             # Percentage of ratings by user:
#             percentage_ratings_df = extract_statistics_rating.get_percentage_ratings_by_user()                    
#             percentage_ratings = percentage_ratings_df.loc[percentage_ratings_df['user_id'] == selected_user, 'percentage_ratings'].iloc[0]
#             # Average of ratings by user:    
#             avg_ratings_df = extract_statistics_rating.get_avg_ratings_by_user()
#             avg_ratings = avg_ratings_df.loc[avg_ratings_df['user_id'] == selected_user, 'avg_ratings'].iloc[0]
#             # Variance of ratings by user:
#             variance_ratings_df = extract_statistics_rating.get_variance_ratings_by_user()
#             variance_ratings = variance_ratings_df.loc[variance_ratings_df['user_id'] == selected_user, 'variance_ratings'].iloc[0]
#             # Standard deviation of ratings by user:
#             sd_ratings_df = extract_statistics_rating.get_sd_items_by_user()                    
#             sd_ratings = sd_ratings_df.loc[sd_ratings_df['user_id'] == selected_user, 'sd_items'].iloc[0]                    
#             rating_statistics_dict['user_id'] = [selected_user]
#             rating_statistics_dict['count'] = [number_ratings]
#             rating_statistics_dict['percentage'] = [percentage_ratings]  
#             rating_statistics_dict['average'] = [avg_ratings]                  
#             rating_statistics_dict['variance'] = [variance_ratings]                  
#             rating_statistics_dict['standard deviation'] = [sd_ratings]      
#             rating_statistics_df = pd.DataFrame(rating_statistics_dict)
#             st.dataframe(rating_statistics_df)
#         except Exception as e:
#             st.error(f"Make sure the rating dataset is in the right format. {e}")
#     else:
#         st.warning("The rating file (rating.csv) has not been uploaded.")