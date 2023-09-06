import streamlit as st

#     if "lars" and "side_lars" in st.session_state:
#         lars = st.session_state["lars"]
#         side_lars = st.session_state["side_lars"]
#         if lars and side_lars:
#             behavior_df = util.load_one_file('behavior')

def evaluate_postfiltering_paradigm(rating_df):
    """
    
    """
    st.write('TODO')
    # lars = st.checkbox('LARS', value=True)
    # st.session_state["lars"] = lars
    # if lars:
    #     side_lars = st.checkbox('SocIal-Distance prEserving', value=True)
    #     st.session_state["side_lars"] = side_lars            
    # if (side_lars) and (not rating_df.empty):
    #     st.sidebar.header("Algorithm selection")
    #     algorithms = st.sidebar.multiselect("Select one or more algorithms", ["KNNBasic", "KNNWithMeans", "KNNWithZScore", "KNNBaseline"], default="KNNBasic")
    #     algo_list = []
    #     for algorithm in algorithms:
    #         algo_params = st_evaluation_rs.select_params(algorithm)
    #         algo_instance = surprise_helpers.create_algorithm(algorithm, algo_params)
    #         algo_list.append(algo_instance)
    #         st.sidebar.markdown("""---""")
    #     st.sidebar.header("Split strategy selection")
    #     strategy = st.sidebar.selectbox("Select a strategy", ["KFold", "RepeatedKFold", "ShuffleSplit", "LeaveOneOut", "PredefinedKFold", "train_test_split"])
    #     strategy_params = st_evaluation_rs.select_split_strategy(strategy)
    #     strategy_instance = surprise_helpers.create_split_strategy(strategy, strategy_params)
    #     data = surprise_helpers.convert_to_surprise_dataset(rating_df)
    #     st.sidebar.header("Metrics selection")                
    #     cast_rating = CastRating(rating_df)              
    #     if cast_rating.is_binary_rating():
    #         metrics = st.sidebar.multiselect("Select one or more cross validation binary metrics", ["Precision", "Recall", "F1_Score", "AUC_ROC"], default="Precision")
    #     else:
    #         metrics = st.sidebar.multiselect("Select one or more cross validation non-binary metrics", ["RMSE", "MSE", "MAE", "FCP", "Precision", "Recall", "F1_Score", "MAP", "NDCG"], default="MAE")
    #     # EVALUATION:
    #     if st.sidebar.button("Evaluate"):
    #         fold_results_df = st_evaluation_rs.evaluate_algo(algo_list, strategy_instance, metrics, data)
    #         # Save the results dataframe in the session state:
    #         st.session_state["fold_results"] = fold_results_df 
    #     # RESULTS:
    #     if "fold_results" in st.session_state:
    #         # Results (folds):
    #         fold_results_df = st.session_state["fold_results"]
    #         st.subheader("Detailed evaluation results (folds and means)")
    #         # Showing result dataframe by folds:
    #         st.dataframe(fold_results_df)        
    #         # Save dataframe:
    #         wf_util.save_df(df_name='fold_evaluation_results', df_value=fold_results_df, extension='csv')

    #         # Results (means):
    #         metric_list = fold_results_df.columns[2:].tolist()
    #         mean_results_df = fold_results_df.groupby('Algorithm')[metric_list].mean().reset_index()
    #         # Showing result dataframe by mean:
    #         st.dataframe(mean_results_df)    
    #         # Save dataframe:                
    #         wf_util.save_df(df_name='mean_evaluation_results', df_value=mean_results_df, extension='csv')
            
    #         # Evaluation figures:
    #         st.subheader("Evaluation graphs (folds and means)")
    #         with_fold = st.selectbox(label="Select one option to plot", options=['Means', 'Folds'])  
    #         algorithm_list = fold_results_df["Algorithm"].unique().tolist()                  
    #         selected_algorithm_list = st.multiselect(label="Select one or more algorithms to plot", options=algorithm_list, default=algorithm_list)
            
    #         # Plotting the graph (by using the "Means" option):
    #         if with_fold == 'Means':
    #             selected_metric_list = st.multiselect(label="Select one or more metrics to plot", options=metric_list, default=metric_list)
    #             # Increasing the maximum value of the Y-axis:
    #             increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)     
    #             # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
    #             df = mean_results_df.loc[mean_results_df['Algorithm'].isin(selected_algorithm_list), ['Algorithm']+selected_metric_list]
    #             # Showing graph:               
    #             if st.button(label='Show graph'):
    #                 st_evaluation_rs.visualize_graph_mean_rs(df, increment_yaxis)
    #                 with st.expander(label='Data to plot in the graphic'):
    #                     st.dataframe(df)
    #         elif with_fold == 'Folds': # Plotting the graph (by using the "Folds" option):
    #             selected_metric = st.selectbox(label="Select one or more metrics to plot", options=metric_list)
    #             # Increasing the maximum value of the Y-axis:
    #             increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
    #             # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
    #             df = fold_results_df.loc[fold_results_df['Algorithm'].isin(selected_algorithm_list), ['Fold', 'Algorithm']+[selected_metric]]                        
    #             # Showing graph:               
    #             if st.button(label='Show graph'):
    #                 st_evaluation_rs.visualize_graph_fold_rs(df, selected_metric, increment_yaxis)
    #                 with st.expander(label='Data to plot in the graphic'):
    #                     st.dataframe(df)
    # else:
    #     st.error(st.warning("The user, item, context, rating and behavior files have not been uploaded."))