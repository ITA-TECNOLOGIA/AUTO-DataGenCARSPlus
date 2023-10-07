import console
import pandas as pd
import plotly.graph_objs as go
import streamlit as st
from datagencars.evaluation.rs_surprise import evaluation, surprise_helpers
from datagencars.existing_dataset.cast_rating.cast_rating import CastRating
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util


def generate(rating_df):
    """
    Evaluating traditional Recommendation Systems.
    """    
    output = st.empty() 
    with console.st_log(output.code):
        if not rating_df.empty:
            st.header('Evaluation of traditional RS')
            print('The rating file has been uploaded.') 
            if 'context_id' in rating_df.columns:
                st.error(f'The uploaded {config.RATING_TYPE} file must not contain contextual information (context_id).')

            # Selecting recommendation systems:
            recommender_list = select_recommendation_algorithms()

            # Selecting the split strategy:
            split_strategy, split_strategy_parameter_dict = select_split_strategy()
            split_strategy_instance = surprise_helpers.create_split_strategy(strategy=split_strategy, params=split_strategy_parameter_dict)
            surprise_data = surprise_helpers.convert_to_surprise_dataset(rating_df)
                   
            # Selecting evaluation metrics:
            metric_list = select_evaluation_metric(rating_df)

            # Evaluating classification algorithm:
            evaluation_result_df = evaluate(surprise_data, recommender_list, split_strategy_instance, metric_list)

            # Showing evaluation results:
            show_evaluation_result(evaluation_result_df)
        else:
            st.error(st.warning("The rating file has not been uploaded."))

def select_recommendation_algorithms():
    """
    Selects a recommendation algorithm.
    """
    st.sidebar.markdown("""---""")
    # Selecting recommendation systems to evaluate:
    recommender_name_list = []
    with st.sidebar.expander(label='**Recommender selection**'):      
        # Basic Recommenders:
        basic_recommender_name = st.multiselect(label='Basic Recommenders:', options=config.BASIC_RS, default=config.BASIC_RS[0])
        recommender_name_list.extend(basic_recommender_name)
        # Collaborative Filtering Recommenders:
        cf_recommender_name = st.multiselect(label='Collaborative Filtering Recommenders:', options=config.CF_RS, default=config.CF_RS[0])
        recommender_name_list.extend(cf_recommender_name)
        # Content-Based Recommenders:
        cb_recommender_type = st.multiselect(label='Content-Based Recommenders:', options=config.CB_RS, default=config.CB_RS[0])
        # recommender_name_list.extend(cb_recommender_type)        
    # Help information:
    help_information.help_rs_algoritms(recommender_name_list)       
    # Parameter settings:
    recommender_list = []
    for rs_algorithm in recommender_name_list:                                          
        rs_parameters_map = select_rs_parameters_map(rs_algorithm)                        
        recommender_instance = surprise_helpers.create_algorithm(rs_algorithm, rs_parameters_map)
        recommender_list.append(recommender_instance)
    print(f'The recommendation algorithm {recommender_name_list} have been selected.')    
    return recommender_list
    
def select_rs_parameters_map(recommendation_algorithm):
    """
    Select parameters of the specified recommendation algorithm.
    :param recommendation_algorithm: A recommendation algorithm.
    :return: A dictionary with parameter values.
    """
    with st.sidebar.expander(label=f'**{recommendation_algorithm} settings**'):      
        ## Basic algorithms:
        # NormalPredictor: Algorithm predicting a random rating based on the distribution of the training set, which is assumed to be normal.
        if recommendation_algorithm == "NormalPredictor":
            return {}
        # BaselineOnly: Algorithm predicting the baseline estimate for given user and item.    
        if recommendation_algorithm == "BaselineOnly":
            return {"bsl_options": {"method": st.selectbox("Baseline method", ["als", "sgd"], key='method_baselineonly'),
                                    "reg_i": st.number_input("Regularization parameter for items", min_value=1, max_value=100, value=10, key='reg_i_baselineonly'),
                                    "reg_u": st.number_input("Regularization parameter for users", min_value=1, max_value=100, value=15, key='reg_u_baselineonly'),
                                    "n_epochs": st.number_input("Number of epochs for optimization algorithms (ALS or SGD)", min_value=10, max_value=100, value=10, key='n_epochs_baselineonly'),
                                    "learning_rate": st.number_input("Controls the step size during the SGD optimization process", min_value=0.0, max_value=0.1, value=0.005, step=0.01, key='learning_rate_baselineonly')}}
        
        ## KNN-based CF algorithms:
        # KNNBasic: A basic collaborative filtering algorithm derived from a basic nearest neighbors approach.
        if recommendation_algorithm == "KNNBasic":
            return {"k": st.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbasic'),
                    "min_k": st.number_input("Minimum number of neighbors", min_value=1, max_value=10, value=1, key='mink_knnbasic'),
                    "sim_options": {"name": st.selectbox("Similarity measure", ["pearson", "cosine", "msd"], key='sim_options_name_knnbasic'),
                                    "user_based": st.selectbox("User-based or item-based similarity", ["user", "item"], key='sim_options_user_based_knnbasic'),
                                    "min_support": st.number_input("Minimum number of common items/users required to compute similarity", min_value=1, max_value=10, value=1, key='sim_options_min_support_knnbasic')}}
        # KNNBaseline: A basic collaborative filtering algorithm taking into account a baseline rating.
        if recommendation_algorithm == "KNNBaseline":
            return {"k": st.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbaseline'),
                    "min_k": st.number_input("Minimum number of neighbors", min_value=1, max_value=10, value=1, key='mink_knnbaseline'),
                    "sim_options": {"name": st.selectbox("Similarity measure", ["pearson", "cosine", "msd"], key='sim_options_name_knnbaseline'),
                                    "user_based": st.selectbox("User-based or item-based similarity", ["user", "item"], key='sim_options_user_based_knnbaseline')},
                    "bsl_options": {"method": st.selectbox("Baseline method", ["als", "sgd"], key='method_knnbaseline'),
                                    "reg_i": st.number_input("Regularization parameter for items", min_value=1, max_value=100, value=10, key='reg_i_knnbaseline'),
                                    "reg_u": st.number_input("Regularization parameter for users", min_value=1, max_value=100, value=15, key='reg_u_knnbaseline'),
                                    "n_epochs": st.number_input("Number of epochs for optimization algorithms (ALS or SGD)", min_value=10, max_value=100, value=10, key='n_epochs_knnbaseline'),
                                    "learning_rate": st.number_input("Controls the step size during the SGD optimization process", min_value=0.0, max_value=0.1, value=0.005, step=0.01, key='learning_rate_knnbaseline')}}
        # KNNWithMeans: A basic collaborative filtering algorithm, taking into account the mean ratings of each user.
        if recommendation_algorithm == "KNNWithMeans":
            return {"k": st.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnwithmeans'),
                    "min_k": st.number_input("Minimum number of neighbors", min_value=1, max_value=10, value=1, key='mink_knnwithmeans'),
                    "sim_options": {"name": st.selectbox("Similarity measure", ["pearson", "cosine", "msd"], key='sim_options_name_knnwithmeans'),
                                    "user_based": st.selectbox("User-based or item-based similarity", ["user", "item"], key='sim_options_user_based_knnwithmeans'),
                                    "min_support": st.number_input("Minimum number of common items/users required to compute similarity", min_value=1, max_value=10, value=1, key='sim_options_min_support_knnwithmeans')}}
        # KNNWithZScore: A basic collaborative filtering algorithm, taking into account the z-score normalization of each user.
        if recommendation_algorithm == "KNNWithZScore":            
            return {"k": st.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnwithzscore'),
                    "min_k": st.number_input("Minimum number of neighbors", min_value=1, max_value=10, value=1, key='mink_knnwithzscore'),
                    "sim_options": {"name": st.selectbox("Similarity measure", ["pearson", "cosine", "msd"], key='sim_options_name_knnwithzscore'),
                                    "user_based": st.selectbox("User-based or item-based similarity", ["user", "item"], key='sim_options_user_based_knnwithzscore'),
                                    "min_support": st.number_input("Minimum number of common items/users required to compute similarity", min_value=1, max_value=10, value=1, key='sim_options_min_support_knnwithzscore')}}
        
        # Matrix factorization-based CF algorithms:    
        # SVD (Singular Value Decomposition): The famous SVD algorithm, as popularized by Simon Funk <https://sifter.org/~simon/journal/20061211.html>:
        if recommendation_algorithm == "SVD":                    
            return {"n_factors": st.number_input("Number of latent factors to use in the matrix factorization", min_value=1, max_value=1000, value=20, key='n_factors_svd'),
                    "n_epochs": st.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_svd'),
                    "lr_all": st.number_input("Learning rate used for SGD optimization", min_value=0.0, max_value=0.1, value=0.007, step=0.01, key='lr_all_svd'),
                    "reg_all": st.number_input("Regularization term for all parameters (it helps prevent overfitting by penalizing large parameter values)", min_value=0.0, max_value=0.1, value=0.02, step=0.01, key='reg_all_svd'),    
                    "biased": st.checkbox("Whether to use baselines (or biases)", value=True, key='biased_svd'),    
                    "init_mean": st.number_input("The mean of the normal distribution for factor vectors initialization", value=0, key='init_mean_svd'),
                    "init_std_dev": st.number_input("The standard deviation of the normal distribution for factor vectors initialization", value=0.1, key='init_std_dev_svd')}
        # SVDpp: The SVD++ algorithm, an extension of :class:SVD taking into account implicit ratings.
        if recommendation_algorithm == "SVDpp":                   
            return {"n_factors": st.number_input("Number of latent factors to use in the matrix factorization", min_value=1, max_value=1000, value=20, key='n_factors_svdpp'),
                    "n_epochs": st.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_svdpp'),
                    "lr_all": st.number_input("Learning rate used for SGD optimization", min_value=0.0, max_value=0.1, value=0.007, step=0.01, key='lr_all_svdpp'),
                    "reg_all": st.number_input("Regularization term for all parameters (it helps prevent overfitting by penalizing large parameter values)", min_value=0.0, max_value=0.1, value=0.02, step=0.01, key='reg_all_svdpp'),
                    "init_mean": st.number_input("The mean of the normal distribution for factor vectors initialization", value=0, key='init_mean_svdpp'),
                    "init_std_dev": st.number_input("The standard deviation of the normal distribution for factor vectors initialization", value=0.1, key='init_std_dev_svdpp')}
        # NMF (Non-Negative Matrix Factorization):     
        if recommendation_algorithm == "NMF":                 
            return {"n_factors": st.number_input("Number of latent factors to use in the matrix factorization", min_value=1, max_value=1000, value=15, key='n_factors_nmf'),
                    "n_epochs": st.number_input("Number of epochs of the SGD procedure", min_value=20, max_value=100, value=50, key='n_epochs_nmf'),
                    "biased": st.checkbox("Whether to use baselines (or biases)", value=False, key='biased_nmf'),
                    "reg_pu": st.number_input("Regularization term for user factors", min_value=0.0, max_value=0.1, value=0.06, key='reg_pu_nmf'),
                    "reg_qi": st.number_input("Regularization term for item factors", min_value=0.0, max_value=0.1, value=0.06, key='reg_qi_nmf'),
                    "reg_bu": st.number_input("Regularization term for bu. Only relevant for biased version.", min_value=0.0, max_value=0.1, value=0.02, key='reg_bu_nmf'),
                    "reg_bi": st.number_input("Regularization term for bi. Only relevant for biased version.", min_value=0.0, max_value=0.1, value=0.02, key='reg_bi_nmf'),
                    "lr_bu": st.number_input("The learning rate for bu. Only relevant for biased version.", min_value=0.0, max_value=0.01, value=0.005, key='lr_bu_nmf'),
                    "lr_bi": st.number_input("The learning rate for bi. Only relevant for biased version.", min_value=-0.0, max_value=0.01, value=0.005, key='lr_bi_nmf'),
                    "init_low": st.number_input("Lower bound for random initialization of factors. Must be greater than 0 to ensure non-negative factors.", min_value=-0.1, max_value=0.0, value=0.0, key='init_low_nmf'),
                    "init_high": st.number_input("Higher bound for random initialization of factors.", min_value=0.0, max_value=1.0, value=1.0, key='init_high_nmf')}
        
        # Clustering-based CF algorithms:  
        # Co-clustering: A collaborative filtering algorithm based on co-clustering.
        if recommendation_algorithm == "CoClustering":            
            return {"n_cltr_u": st.number_input("Number of user clusters", min_value=1, max_value=1000, value=3, key='n_cltr_u_coclustering'),
                    "n_cltr_i": st.number_input("Number of item clusters", min_value=1, max_value=1000, value=3, key='n_cltr_i_coclustering'),
                    "n_epochs": st.number_input("Number of iteration of the optimization loop", min_value=1, max_value=1000, value=20, key='n_epochs_coclustering')}
        # SlopeOne:    
        if recommendation_algorithm == "SlopeOne":
            return {}

def select_split_strategy():
    """
    Selects split strategies (ShuffleSplit, KFold or LeaveOneOut) to evaluate recommendation algorithm.
    :return: A dictionary with parameter values.
    """    
    with st.sidebar.expander(label=f'**Split strategy selection**'):          
        split_strategy = st.selectbox(label="Select a strategy", options=config.CROSS_VALIDATION_STRATEGIES) 
        split_strategy_parameter_dict = {}
        if split_strategy == "KFold":
            st.markdown("""A basic cross-validation iterator. Each fold is used once as a testset while the k - 1 remaining folds are used for training.""")
            split_strategy_parameter_dict = {"n_splits": st.number_input("Number of folds", min_value=2, max_value=10, value=5),
                    "shuffle": st.checkbox("Shuffle?")}
        elif split_strategy == "RepeatedKFold":
            st.markdown("""Repeats KFold n times with different randomization in each repetition.""")
            split_strategy_parameter_dict = {"n_splits": st.number_input("Number of folds", min_value=2, max_value=10, value=5),
                                            "n_repeats": st.number_input("Number of repeats", min_value=1, max_value=10, value=1)}
        elif split_strategy == "ShuffleSplit":
            st.markdown("""A basic cross-validation iterator with random trainsets and testsets. Contrary to other cross-validation strategies, random splits do not guarantee that all folds will be different, although this is still very likely for sizeable datasets.""")
            split_strategy_parameter_dict = {"n_splits": st.number_input("Number of folds", min_value=2, max_value=10, value=5),
                                            "test_size": st.number_input("Test size", min_value=0.1, max_value=0.9, step=0.1, value=0.2),
                                            "shuffle": st.checkbox("Shuffle?")}
        elif split_strategy == "LeaveOneOut":
            st.markdown("""Cross-validation iterator where each user has exactly one rating in the testset. Contrary to other cross-validation strategies, LeaveOneOut does not guarantee that all folds will be different, although this is still very likely for sizeable datasets.""")
            split_strategy_parameter_dict = {"n_splits": st.number_input("Number of folds", min_value=2, max_value=10, value=5),
                                            "min_n_ratings": st.number_input("Minimum number of ratings for each user (trainset)", min_value=0, max_value=10000, value=0)}    
    return split_strategy, split_strategy_parameter_dict

def select_evaluation_metric(rating_df):
    """
    Selects evaluation metrics.
    :return: A list with the evaluation metrics.
    """ 
    with st.sidebar.expander(label=f'**Metrics selection**'):    
        cast_rating = CastRating(rating_df)              
        if cast_rating.is_binary_rating():
            metric_list = st.multiselect(label="Select one or more binary metrics", options=config.BINARY_RATING_METRICS, default=config.DEFAULT_BINARY_RATING_METRICS)
        else:
            metric_list = st.multiselect(label="Select one or more non-binary metrics", options=config.PREFERENCIAL_RATING_METRICS, default=config.DEFAULT_PREFERENCIAL_RATING_METRICS)
    return metric_list

def evaluate(surprise_data, recommender_list, split_strategy_instance, metric_list):
    """
    Evaluates recommendation algorithms.
    :param knowledge_base_df: The recommendation knowledge base.
    :param recommender_list: The list of recommenders to evaluate.
    :param split_strategy_instance: A object of the split strategy to use during the evaluation.
    :param metrics: The list of metrics to use during the evaluation.    
    :return: A dataframe with evaluation results.
    """ 
    evaluation_result_df = pd.DataFrame()
    if surprise_data:
        if st.sidebar.button("Evaluate"):
            # fold_results_df = evaluate_algo(algo_list, strategy_instance, metrics, data)
            evaluation_result_list = []
            # To count the number of folds for each algorithm:
            fold_counter = {}
            fold_count = 0
            with st.spinner("Evaluating algorithms..."):
                for recommender in recommender_list:
                    fold_count += 1
                    cross_validate_results = evaluation.cross_validate(algo=recommender, data=surprise_data, measures=metric_list, cv=split_strategy_instance)
                    for i in range(split_strategy_instance.n_splits):
                        row = {}
                        algo_name = type(recommender).__name__
                        row["Algorithm"] = algo_name

                        # Modify the name of the metrics to be more readable:
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
                        evaluation_result_list.append(row)
            evaluation_result_df = pd.DataFrame(evaluation_result_list)
            cols = ["Fold"] + [col for col in evaluation_result_df.columns if col != "Fold"] # Move the "Fold" column to the first position
            evaluation_result_df = evaluation_result_df[cols]
            # Save the results dataframe in the session state:
            st.session_state["evaluation_result_df"] = evaluation_result_df 
            print('The recommendation algorithms have been evaluated.')
    return evaluation_result_df

def show_evaluation_result(evaluation_result_df):
    """
    Showing evaluation results.
    :param evaluation_result_df: The dataframe with evaluation results.    
    """ 
    if "evaluation_result_df" in st.session_state:
        # Results (folds):
        evaluation_result_df = st.session_state["evaluation_result_df"]
        st.subheader("Detailed evaluation results (folds and means)")
        # Showing result dataframe by folds:
        st.dataframe(evaluation_result_df)        
        # Save dataframe:
        wf_util.save_df(df_name='fold_evaluation_results', df_value=evaluation_result_df, extension='csv')

        # Results (means):
        metric_list = evaluation_result_df.columns[2:].tolist()
        mean_results_df = evaluation_result_df.groupby('Algorithm')[metric_list].mean().reset_index()
        # Showing result dataframe by mean:
        st.dataframe(mean_results_df)    
        # Save dataframe:                
        wf_util.save_df(df_name='mean_evaluation_results', df_value=mean_results_df, extension='csv')            

        # Evaluation figures:
        st.subheader("Evaluation graphs (folds and means)")
        with_fold = st.selectbox(label="Select one option to plot", options=['Means', 'Folds'])  
        algorithm_list = evaluation_result_df["Algorithm"].unique().tolist()                  
        selected_algorithm_list = st.multiselect(label="Select one or more algorithms to plot", options=algorithm_list, default=algorithm_list)            
        # Plotting the graph (by using the "Means" option):
        if with_fold == 'Means':
            selected_metric_list = st.multiselect(label="Select one or more metrics to plot", options=metric_list, default=metric_list)
            # Increasing the maximum value of the Y-axis:
            increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)     
            # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
            df = mean_results_df.loc[mean_results_df['Algorithm'].isin(selected_algorithm_list), ['Algorithm']+selected_metric_list]
            # Showing graph:               
            if st.button(label='Show graph'):
                draw_graph_by_mean(df, increment_yaxis)
                with st.expander(label='Data to plot in the graphic'):
                    st.dataframe(df)
        elif with_fold == 'Folds': # Plotting the graph (by using the "Folds" option):
            selected_metric = st.selectbox(label="Select one or more metrics to plot", options=metric_list)
            # Increasing the maximum value of the Y-axis:
            increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
            # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
            df = evaluation_result_df.loc[evaluation_result_df['Algorithm'].isin(selected_algorithm_list), ['Fold', 'Algorithm']+[selected_metric]]                        
            # Showing graph:               
            if st.button(label='Show graph'):
                draw_graph_by_fold(df, selected_metric, increment_yaxis)
                with st.expander(label='Data to plot in the graphic'):
                    st.dataframe(df)

def draw_graph_by_mean(df, increment_yaxis):
    """
    Visualize mean results of the evaluation of recommendation algorithms.   
    :param df: A dataframe with evaluation mean results.
    :param increment_yaxis: A float value to increase the maximum value of the Y-axis.    
    """
    # Create trace for each column:
    fig = go.Figure()
    for column in df.columns[1:]:
        fig.add_trace(go.Bar(x=df['Algorithm'], y=df[column], name=column))      
    # Create figure:
    selected_metric_list = df.columns[1:].tolist()
    fig.update_layout(title='Performance Comparison of Recommendation Algorithms', xaxis_title='Recommendation Algorithm', yaxis_title='Performance', legend=dict(title="Metrics"), barmode='group', yaxis_range=[0, df[selected_metric_list].max().max()+increment_yaxis])
    # Show plot:                        
    st.plotly_chart(fig, use_container_width=True)

def draw_graph_by_fold(df, metric, increment_yaxis):
    """
    Visualize fold results by metric of the evaluation of recommendation algorithms.   
    :param df: A dataframe with evaluation results by fold.
    :param metric: The metric measure.
    :param increment_yaxis: A float value to increase the maximum value of the Y-axis.    
    """
    algorithms = df["Algorithm"].unique()
    fig = go.Figure()
    for algorithm in algorithms:
        # Filter the dataframe for the current algorithm
        filtered_df = df[df["Algorithm"] == algorithm]
        # Create the line chart for the current metric
        fig.add_trace(go.Scatter(x=filtered_df["Fold"], y=filtered_df[metric], name=algorithm))
    fig.update_layout(xaxis_title="Fold", yaxis_title="Performance", legend=dict(title="Recommendation algorithms"), yaxis_range=[0, df[metric].max().max()+increment_yaxis])
    st.plotly_chart(fig, use_container_width=True)
    