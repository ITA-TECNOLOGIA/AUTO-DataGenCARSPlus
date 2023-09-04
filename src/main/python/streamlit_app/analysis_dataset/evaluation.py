import streamlit as st

def generation(with_context):
    pass


# st.header('Evaluation')  
# # CARS Evaluation:        
# if with_context:
#     if (not rating_df.empty) and (not item_df.empty) and (not context_df.empty):
#         st.sidebar.markdown("""---""")
#         # SELECTING PARADIGM TO EVALUATE:
#         st.sidebar.markdown('**CARS paradigm selection**')
#         paradigm = st.sidebar.selectbox("Select one paradigm", ["Contextual Modeling", "Pre-filtering", "Post-filtering"])
#         lars = st.sidebar.checkbox('LARS', value=True)
#         st.session_state["lars"] = lars
#         if lars:
#             side_lars = st.sidebar.checkbox('SocIal-Distance prEserving', value=True)
#             st.session_state["side_lars"] = side_lars
#         st.sidebar.markdown("""---""")
#         if paradigm == "Contextual Modeling":
#             # SELECTING CONTEXTUAL FEATURES:
#             st.sidebar.markdown('**Contextual features selection**')
#             item_feature_df = util.select_contextual_features(df=item_df, label="item")                    
#             context_feature_df = util.select_contextual_features(df=context_df, label="context")
#             # Building knowledge base:                    
#             try:
#                 merged_df = rating_df.merge(item_feature_df, on='item_id').merge(context_feature_df, on='context_id')
#                 merged_df.drop('context_id', axis=1, inplace=True)
#             except KeyError as e:
#                 st.error(f"The rating, user, item and context datasets do not have '_id' columns in common. {e}")                    
#             st.sidebar.markdown("""---""")
#             # SELECTING CLASSIFIER:
#             st.sidebar.markdown('**Classifier selection**')
#             classifier_name_list = st.sidebar.multiselect("Select one or more classifiers", ["KNeighborsClassifier", "SVC", "GaussianNB", "RandomForestClassifier", "KMeans", "HistGradientBoostingClassifier"], default="KNeighborsClassifier")
#             # Replacing some values and building classifiers.
#             classifier_list = []
#             st.sidebar.write("-0.5 values will be replaced with None")
#             # Help information:
#             with st.expander(label='Help information'): 
#                 for classifier_name in classifier_name_list:
#                     classifier_params = util.replace_with_none(util.select_params_contextual(classifier_name))
#                     if classifier_name == 'KNeighborsClassifier':
#                         st.markdown("""- ``` KNeighborsClassifier ```: Classifier implementing the k-nearest neighbors vote.""")
#                     if classifier_name == 'SVC':
#                         st.markdown("""- ``` SVC ```: C-Support Vector Classification. The implementation is based on libsvm.""")
#                     if classifier_name == 'GaussianNB':
#                         st.markdown("""- ``` GaussianNB ```: Gaussian Naive Bayes.""")
#                     if classifier_name == 'RandomForestClassifier':
#                         st.markdown("""- ``` RandomForestClassifier ```: A random forest classifier. A random forest is a meta estimator that fits a number of decision tree classifiers on various sub-samples of the dataset and uses averaging to improve the predictive accuracy and control over-fitting.""")
#                     if classifier_name == 'KMeans':
#                         st.markdown("""- ``` KMeans ```: K-Means clustering.""")
#                     if classifier_name == 'HistGradientBoostingClassifier':
#                         st.markdown("""- ``` HistGradientBoostingClassifier ```: Histogram-based Gradient Boosting Classification Tree. This estimator has native support for missing values (NaNs).""")
#                     st.markdown("""These algorithms are implemented in the [scikit-learn](https://scikit-learn.org/stable/supervised_learning.html#supervised-learning) python library.""")                                             
#                     # PARAMETER SETTINGS:                            
#                     classifier_instance = sklearn_helpers.create_algorithm(classifier_name, classifier_params)
#                     classifier_list.append(classifier_instance)
#                     st.sidebar.markdown("""---""")
#             # CROSS VALIDATION:
#             st.sidebar.markdown('**Split strategy selection**')
#             strategy = st.sidebar.selectbox("Select a strategy", ["KFold", "ShuffleSplit", "LeaveOneOut"]) # , "PredefinedKFold", "train_test_split", "RepeatedKFold", 
#             strategy_params = util.select_split_strategy_contextual(strategy)
#             strategy_instance = sklearn_helpers.create_split_strategy(strategy, strategy_params)
#             st.sidebar.markdown("""---""")
#             # METRICS:
#             st.sidebar.markdown('**Metrics selection**')  
#             metrics = st.sidebar.multiselect("Select one or more metrics", config.SCIKIT_LEARN_METRICS, default="Precision")
#             st.sidebar.markdown("""---""")
#             # EVALUATION:
#             st.sidebar.markdown('**Target user**')
#             # Extract unique user_ids and add "All users" option
#             user_ids = sorted(rating_df['user_id'].unique().tolist())
#             user_options = ["All users"] + user_ids
#             selected_users = st.sidebar.multiselect("Select one or more users or 'All users'", options=user_options, default="All users")
#             if st.sidebar.button("Evaluate"):
#                 if "All users" in selected_users:
#                     target_user_ids = None
#                 else:
#                     target_user_ids = selected_users                            
#                 fold_results_df = sklearn_helpers.evaluate(merged_df, classifier_list, strategy_instance, metrics, target_user_ids)
#                 st.session_state["fold_results"] = fold_results_df #Save the results dataframe in the session state
#             # RESULTS:
#             if "fold_results" in st.session_state:
#                 # Results (folds):
#                 fold_results_df = st.session_state["fold_results"]
#                 st.subheader("Detailed evaluation results (folds and means)")
#                 st.dataframe(fold_results_df)                    
#                 link_fold_result = f'<a href="data:file/csv;base64,{base64.b64encode(fold_results_df.to_csv(index=False).encode()).decode()}" download="fold_evaluation_results.csv">Download results</a>'
#                 st.markdown(link_fold_result, unsafe_allow_html=True)
#                 # Results (means):
#                 metric_list = fold_results_df.columns[3:].tolist()                 
#                 mean_results_df = fold_results_df.groupby(['User','Algorithm'])[metric_list].mean().reset_index()
#                 st.dataframe(mean_results_df)                    
#                 link_mean_result = f'<a href="data:file/csv;base64,{base64.b64encode(mean_results_df.to_csv(index=False).encode()).decode()}" download="mean_evaluation_results.csv">Download results</a>'
#                 st.markdown(link_mean_result, unsafe_allow_html=True)
#                 # Evaluation figures:
#                 st.subheader("Evaluation graphs (folds and means)")
#                 with_fold = st.selectbox(label="Select one option to plot", options=['Means', 'Folds']) 
#                 col_algorithm, col_metric, col_user = st.columns(3)
#                 with col_algorithm:
#                     st.session_state['selected_algorithm_list'] = st.multiselect(label="Select an algorithm", options=fold_results_df["Algorithm"].unique().tolist())
#                 with col_metric:                            
#                     st.session_state['selected_metric_list'] = st.multiselect(label="Select a metric", options=metric_list)
#                 with col_user:                                                        
#                     st.session_state['selected_users_list'] = st.multiselect(label="Select a user", options=selected_users)  
#                 # Increasing the maximum value of the Y-axis:
#                 increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
#                 # Plotting the graph (by using the "Means" option):
#                 if with_fold == 'Means':                             
#                     # Showing graph:               
#                     if st.button(label='Show graph'):
#                         util.visualize_graph_mean_cars(fold_results_df, st.session_state['selected_algorithm_list'], st.session_state['selected_metric_list'], st.session_state['selected_users_list'], increment_yaxis)
#                         # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
#                         df = mean_results_df.loc[mean_results_df['Algorithm'].isin(st.session_state['selected_algorithm_list']), ['User', 'Algorithm']+st.session_state['selected_metric_list']]
#                         with st.expander(label='Data to plot in the graphic'):
#                             st.dataframe(df)
#                 elif with_fold == 'Folds': # Plotting the graph (by using the "Folds" option):                            
#                     # Showing graph:               
#                     if st.button(label='Show graph'):                                
#                         util.visualize_graph_fold_cars(fold_results_df, st.session_state['selected_algorithm_list'], st.session_state['selected_metric_list'], st.session_state['selected_users_list'], increment_yaxis)
#                         # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:                                
#                         df = fold_results_df.loc[fold_results_df['Algorithm'].isin(st.session_state['selected_algorithm_list']), ['User', 'Fold', 'Algorithm']+st.session_state['selected_metric_list']]
#                         with st.expander(label='Data to plot in the graphic'):
#                             st.dataframe(df)
#         elif paradigm == "Post-filtering":
#             if side_lars and (not user_df.empty) and (not item_df.empty) and (not context_df.empty) and (not rating_df.empty) and (not behavior_df.empty):
#                 st.sidebar.header("Algorithm selection")
#                 algorithms = st.sidebar.multiselect("Select one or more algorithms", ["KNNBasic", "KNNWithMeans", "KNNWithZScore", "KNNBaseline"], default="KNNBasic")
#                 algo_list = []
#                 for algorithm in algorithms:
#                     algo_params = util.select_params(algorithm)
#                     algo_instance = surprise_helpers.create_algorithm(algorithm, algo_params)
#                     algo_list.append(algo_instance)
#                     st.sidebar.markdown("""---""")
#                 st.sidebar.header("Split strategy selection")
#                 strategy = st.sidebar.selectbox("Select a strategy", ["KFold", "RepeatedKFold", "ShuffleSplit", "LeaveOneOut", "PredefinedKFold", "train_test_split"])
#                 strategy_params = util.select_split_strategy(strategy)
#                 strategy_instance = surprise_helpers.create_split_strategy(strategy, strategy_params)
#                 data = surprise_helpers.convert_to_surprise_dataset(rating_df)
#                 st.sidebar.header("Metrics selection")
#                 if binary_ratings.is_binary_rating(rating_df):
#                     metrics = st.sidebar.multiselect("Select one or more cross validation binary metrics", ["Precision", "Recall", "F1_Score", "AUC_ROC"], default="Precision")
#                 else:
#                     metrics = st.sidebar.multiselect("Select one or more cross validation non-binary metrics", ["RMSE", "MSE", "MAE", "FCP", "Precision", "Recall", "F1_Score", "MAP", "NDCG"], default="MAE")
#                 # EVALUATION:
#                 if st.sidebar.button("Evaluate"):
#                     fold_results_df = util.evaluate_algo(algo_list, strategy_instance, metrics, data)
#                     st.session_state["fold_results"] = fold_results_df #Save the results dataframe in the session state
#                 # RESULTS:
#                 if "fold_results" in st.session_state:
#                     # Results (folds):
#                     fold_results_df = st.session_state["fold_results"]
#                     st.subheader("Detailed evaluation results (folds and means)")
#                     st.dataframe(fold_results_df)                    
#                     link_fold_result = f'<a href="data:file/csv;base64,{base64.b64encode(fold_results_df.to_csv(index=False).encode()).decode()}" download="fold_evaluation_results.csv">Download results</a>'
#                     st.markdown(link_fold_result, unsafe_allow_html=True)
#                     # Results (means):
#                     metric_list = fold_results_df.columns[2:].tolist()
#                     mean_results_df = fold_results_df.groupby('Algorithm')[metric_list].mean().reset_index()
#                     st.dataframe(mean_results_df)                    
#                     link_mean_result = f'<a href="data:file/csv;base64,{base64.b64encode(mean_results_df.to_csv(index=False).encode()).decode()}" download="mean_evaluation_results.csv">Download results</a>'
#                     st.markdown(link_mean_result, unsafe_allow_html=True)
#                     # Evaluation figures:
#                     st.subheader("Evaluation graphs (folds and means)")
#                     with_fold = st.selectbox(label="Select one option to plot", options=['Means', 'Folds'])  
#                     algorithm_list = fold_results_df["Algorithm"].unique().tolist()                  
#                     selected_algorithm_list = st.multiselect(label="Select one or more algorithms to plot", options=algorithm_list, default=algorithm_list)
                    
#                     # Plotting the graph (by using the "Means" option):
#                     if with_fold == 'Means':
#                         selected_metric_list = st.multiselect(label="Select one or more metrics to plot", options=metric_list, default=metric_list)
#                         # Increasing the maximum value of the Y-axis:
#                         increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)     
#                         # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
#                         df = mean_results_df.loc[mean_results_df['Algorithm'].isin(selected_algorithm_list), ['Algorithm']+selected_metric_list]
#                         # Showing graph:               
#                         if st.button(label='Show graph'):
#                             util.visualize_graph_mean_rs(df, increment_yaxis)
#                             with st.expander(label='Data to plot in the graphic'):
#                                 st.dataframe(df)
#                     elif with_fold == 'Folds': # Plotting the graph (by using the "Folds" option):
#                         selected_metric = st.selectbox(label="Select one or more metrics to plot", options=metric_list)
#                         # Increasing the maximum value of the Y-axis:
#                         increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
#                         # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
#                         df = fold_results_df.loc[fold_results_df['Algorithm'].isin(selected_algorithm_list), ['Fold', 'Algorithm']+[selected_metric]]                        
#                         # Showing graph:               
#                         if st.button(label='Show graph'):
#                             util.visualize_graph_fold_rs(df, selected_metric, increment_yaxis)
#                             with st.expander(label='Data to plot in the graphic'):
#                                 st.dataframe(df)
#             else:
#                 st.error(st.warning("The user, item, context, rating and behavior files have not been uploaded."))
#         else:
#             st.write("TODO: pre-filtering")
#     else:
#         st.warning("The item, context and rating files have not been uploaded.")
# else:
#     # Traditional RS Evaluation:
#     if not rating_df.empty:
#         st.sidebar.markdown("""---""")
#         # SELECTING RS TO EVALUATE:                
#         st.sidebar.markdown('**Recommendation Systems selection**')
#         recommender_name_list = []
#         # Basic Recommenders:
#         basic_recommender_name = st.sidebar.multiselect(label='Basic Recommenders:', options=['BaselineOnly', 'NormalPredictor'])
#         recommender_name_list.extend(basic_recommender_name)
#         # Collaborative Filtering Recommenders:
#         cf_recommender_name = st.sidebar.multiselect(label='Collaborative Filtering Recommenders:', options=['KNNBasic', 'KNNWithMeans', 'KNNWithZScore', 'KNNBaseline', 'SVD', 'SVDpp', 'NMF', 'SlopeOne', 'CoClustering'])
#         recommender_name_list.extend(cf_recommender_name)
#         # Content-Based Recommenders:
#         cb_recommender_type = st.sidebar.multiselect(label='Content-Based Recommenders:', options=['PENDING TODO'])
#         # recommender_name_list.extend(cb_recommender_type)
#         # Help information:
#         with st.expander(label='Help information'):                    
#             for recommender_name in recommender_name_list:                        
#                 if recommender_name == 'BaselineOnly':
#                     st.markdown("""- ``` BaselineOnly ```: Algorithm predicting the baseline estimate for given user and item.""")
#                 if recommender_name == 'NormalPredictor':
#                     st.markdown("""- ``` NormalPredictor ```: Algorithm predicting a random rating based on the distribution of the training set, which is assumed to be normal.""")
#                 if recommender_name == 'KNNBasic':
#                     st.markdown("""- ``` KNNBasic ```: A basic collaborative filtering algorithm derived from a basic nearest neighbors approach.""")
#                 if recommender_name == 'KNNWithMeans':
#                     st.markdown("""- ``` KNNWithMeans ```: A basic collaborative filtering algorithm, taking into account the mean ratings of each user.""")
#                 if recommender_name == 'KNNWithZScore':
#                     st.markdown("""- ``` KNNWithZScore ```: A basic collaborative filtering algorithm, taking into account the z-score normalization of each user.""")
#                 if recommender_name == 'KNNBaseline':
#                     st.markdown("""- ``` KNNBaseline ```: A basic collaborative filtering algorithm taking into account a baseline rating.""")
#                 if recommender_name == 'SVD':
#                     st.markdown("""- ``` SVD ```: The famous SVD algorithm, as popularized by Simon Funk during the Netflix Prize. When baselines are not used, this is equivalent to Probabilistic Matrix Factorization""")
#                 if recommender_name == 'SVDpp':
#                     st.markdown("""- ``` SVDpp ```: The SVD++ algorithm, an extension of SVD taking into account implicit ratings.""")
#                 if recommender_name == 'NMF':
#                     st.markdown("""- ``` NMF ```:  A collaborative filtering algorithm based on Non-negative Matrix Factorization.""")
#                 if recommender_name == 'SlopeOne':
#                     st.markdown("""- ``` SlopeOne ```: A simple yet accurate collaborative filtering algorithm. This is a straightforward implementation of the SlopeOne algorithm [LM07]. [LM07] Daniel Lemire and Anna Maclachlan. [Slope one predictors for online rating-based collaborative filtering](https://arxiv.org/abs/cs/0702144). 2007.""")
#                 if recommender_name == 'CoClustering':
#                     st.markdown("""- ``` CoClustering ```: A collaborative filtering algorithm based on co-clustering. This is a straightforward implementation of [GM05]. [GM05] Thomas George and Srujana Merugu. [A scalable collaborative filtering framework based on co-clustering](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.113.6458&rep=rep1&type=pdf). 2005.""")
#             st.markdown("""These algorithms are implemented in the [surprise](https://github.com/NicolasHug/Surprise) python library.""")                                             
#         # PARAMETER SETTINGS:
#         algo_list = []
#         for algorithm in recommender_name_list:                                  
#             algo_params = util.select_params(algorithm)                        
#             algo_instance = surprise_helpers.create_algorithm(algorithm, algo_params)
#             algo_list.append(algo_instance)
#         st.sidebar.markdown("""---""")            
#         # CROSS VALIDATION:
#         st.sidebar.markdown('**Split strategy selection**')
#         strategy = st.sidebar.selectbox("Select a strategy", ["KFold", "RepeatedKFold", "ShuffleSplit", "LeaveOneOut"]) # , "PredefinedKFold", "train_test_split"
#         strategy_params = util.select_split_strategy(strategy)
#         strategy_instance = surprise_helpers.create_split_strategy(strategy, strategy_params)
#         data = surprise_helpers.convert_to_surprise_dataset(rating_df)
#         st.sidebar.markdown("""---""")
#         # METRICS:
#         st.sidebar.markdown('**Metrics selection**')                
#         if binary_ratings.is_binary_rating(rating_df):
#             metrics = st.sidebar.multiselect("Select one or more binary metrics", ["Precision", "Recall", "F1_Score", "AUC_ROC"], default=["Precision", "Recall", "F1_Score"])
#         else:
#             metrics = st.sidebar.multiselect("Select one or more non-binary metrics", ["MAE", "Precision", "Recall", "F1_Score", "RMSE", "MSE", "FCP", "MAP", "NDCG"], default=["MAE", "Precision", "Recall", "F1_Score"])
#         # EVALUATION:
#         if st.sidebar.button("Evaluate"):
#             fold_results_df = util.evaluate_algo(algo_list, strategy_instance, metrics, data)
#             st.session_state["fold_results"] = fold_results_df #Save the results dataframe in the session state
#         # RESULTS:
#         if "fold_results" in st.session_state:
#             # Results (folds):
#             fold_results_df = st.session_state["fold_results"]
#             st.subheader("Detailed evaluation results (folds and means)")
#             st.dataframe(fold_results_df)                    
#             link_fold_result = f'<a href="data:file/csv;base64,{base64.b64encode(fold_results_df.to_csv(index=False).encode()).decode()}" download="fold_evaluation_results.csv">Download results</a>'
#             st.markdown(link_fold_result, unsafe_allow_html=True)
#             # Results (means):
#             metric_list = fold_results_df.columns[2:].tolist()
#             mean_results_df = fold_results_df.groupby('Algorithm')[metric_list].mean().reset_index()
#             st.dataframe(mean_results_df)                    
#             link_mean_result = f'<a href="data:file/csv;base64,{base64.b64encode(mean_results_df.to_csv(index=False).encode()).decode()}" download="mean_evaluation_results.csv">Download results</a>'
#             st.markdown(link_mean_result, unsafe_allow_html=True)
#             # Evaluation figures:
#             st.subheader("Evaluation graphs (folds and means)")
#             with_fold = st.selectbox(label="Select one option to plot", options=['Means', 'Folds'])  
#             algorithm_list = fold_results_df["Algorithm"].unique().tolist()                  
#             selected_algorithm_list = st.multiselect(label="Select one or more algorithms to plot", options=algorithm_list, default=algorithm_list)
            
#             # Plotting the graph (by using the "Means" option):
#             if with_fold == 'Means':
#                 selected_metric_list = st.multiselect(label="Select one or more metrics to plot", options=metric_list, default=metric_list)
#                 # Increasing the maximum value of the Y-axis:
#                 increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)     
#                 # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
#                 df = mean_results_df.loc[mean_results_df['Algorithm'].isin(selected_algorithm_list), ['Algorithm']+selected_metric_list]
#                 # Showing graph:               
#                 if st.button(label='Show graph'):
#                     util.visualize_graph_mean_rs(df, increment_yaxis)
#                     with st.expander(label='Data to plot in the graphic'):
#                         st.dataframe(df)
#             elif with_fold == 'Folds': # Plotting the graph (by using the "Folds" option):
#                 selected_metric = st.selectbox(label="Select one or more metrics to plot", options=metric_list)
#                 # Increasing the maximum value of the Y-axis:
#                 increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
#                 # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
#                 df = fold_results_df.loc[fold_results_df['Algorithm'].isin(selected_algorithm_list), ['Fold', 'Algorithm']+[selected_metric]]                        
#                 # Showing graph:               
#                 if st.button(label='Show graph'):
#                     util.visualize_graph_fold_rs(df, selected_metric, increment_yaxis)
#                     with st.expander(label='Data to plot in the graphic'):
#                         st.dataframe(df)
#     else:
#         st.error(st.warning("The rating file has not been uploaded."))