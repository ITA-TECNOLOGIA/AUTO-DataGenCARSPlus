import pandas as pd
import plotly.graph_objs as go
import streamlit as st
from datagencars.evaluation.rs_surprise import evaluation, surprise_helpers
from datagencars.existing_dataset.cast_rating.cast_rating import CastRating
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util


def evaluate():
    """
    Evaluating traditional Recommendation Systems.
    """
    st.header('Evaluation of traditional RS')

    # Loading rating file:
    rating_df = wf_util.load_one_file(config.RATING_TYPE, wf_type='evaluation_rs')
    st.sidebar.markdown("""---""")

    if not rating_df.empty:
        # SELECTING RS TO EVALUATE:                
        st.sidebar.markdown('**Recommendation Systems selection**')
        recommender_name_list = []
        # Basic Recommenders:
        basic_recommender_name = st.sidebar.multiselect(label='Basic Recommenders:', options=config.BASIC_RS)
        recommender_name_list.extend(basic_recommender_name)
        # Collaborative Filtering Recommenders:
        cf_recommender_name = st.sidebar.multiselect(label='Collaborative Filtering Recommenders:', options=config.CF_RS)
        recommender_name_list.extend(cf_recommender_name)
        # Content-Based Recommenders:
        cb_recommender_type = st.sidebar.multiselect(label='Content-Based Recommenders:', options=config.CB_RS)
        # recommender_name_list.extend(cb_recommender_type)
        # Help information:
        help_information.help_rs_algoritms(recommender_name_list)
        
        # PARAMETER SETTINGS:
        algo_list = []
        for algorithm in recommender_name_list:                                  
            algo_params = select_params(algorithm)                        
            algo_instance = surprise_helpers.create_algorithm(algorithm, algo_params)
            algo_list.append(algo_instance)
        st.sidebar.markdown("""---""")

        # CROSS VALIDATION:
        st.sidebar.markdown('**Split strategy selection**')
        strategy = st.sidebar.selectbox(label="Select a strategy", options=config.CROSS_VALIDATION_STRATEGIES) 
        strategy_params = select_split_strategy(strategy)
        strategy_instance = surprise_helpers.create_split_strategy(strategy, strategy_params)
        data = surprise_helpers.convert_to_surprise_dataset(rating_df)
        st.sidebar.markdown("""---""")

        # METRICS:
        st.sidebar.markdown('**Metrics selection**')
        cast_rating = CastRating(rating_df)              
        if cast_rating.is_binary_rating():
            metrics = st.sidebar.multiselect(label="Select one or more binary metrics", options=config.BINARY_RATING_METRICS, default=config.DEFAULT_BINARY_RATING_METRICS)
        else:
            metrics = st.sidebar.multiselect(label="Select one or more non-binary metrics", options=config.PREFERENCIAL_RATING_METRICS, default=config.DEFAULT_PREFERENCIAL_RATING_METRICS)

        # EVALUATION:
        if st.sidebar.button("Evaluate"):
            fold_results_df = evaluate_algo(algo_list, strategy_instance, metrics, data)
            # Save the results dataframe in the session state:
            st.session_state["fold_results"] = fold_results_df 

        # RESULTS:
        if "fold_results" in st.session_state:
            # Results (folds):
            fold_results_df = st.session_state["fold_results"]
            st.subheader("Detailed evaluation results (folds and means)")
            # Showing result dataframe by folds:
            st.dataframe(fold_results_df)        
            # Save dataframe:
            wf_util.save_df(df_name='fold_evaluation_results', df_value=fold_results_df, extension='csv')

            # Results (means):
            metric_list = fold_results_df.columns[2:].tolist()
            mean_results_df = fold_results_df.groupby('Algorithm')[metric_list].mean().reset_index()
            # Showing result dataframe by mean:
            st.dataframe(mean_results_df)    
            # Save dataframe:                
            wf_util.save_df(df_name='mean_evaluation_results', df_value=mean_results_df, extension='csv')            

            # Evaluation figures:
            st.subheader("Evaluation graphs (folds and means)")
            with_fold = st.selectbox(label="Select one option to plot", options=['Means', 'Folds'])  
            algorithm_list = fold_results_df["Algorithm"].unique().tolist()                  
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
                    visualize_graph_mean_rs(df, increment_yaxis)
                    with st.expander(label='Data to plot in the graphic'):
                        st.dataframe(df)
            elif with_fold == 'Folds': # Plotting the graph (by using the "Folds" option):
                selected_metric = st.selectbox(label="Select one or more metrics to plot", options=metric_list)
                # Increasing the maximum value of the Y-axis:
                increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
                # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
                df = fold_results_df.loc[fold_results_df['Algorithm'].isin(selected_algorithm_list), ['Fold', 'Algorithm']+[selected_metric]]                        
                # Showing graph:               
                if st.button(label='Show graph'):
                    visualize_graph_fold_rs(df, selected_metric, increment_yaxis)
                    with st.expander(label='Data to plot in the graphic'):
                        st.dataframe(df)
    else:
        st.error(st.warning("The rating file has not been uploaded."))

def select_params(algorithm):
    """
    Select parameters of the specified recommendation algorithm.
    :param algorithm: A recommendation algorithm.
    :return: A dictionary with parameter values.
    """
    if algorithm == "SVD":
        st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
        return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_svd'),
                "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_svd'),
                "lr_all": st.sidebar.number_input("Learning rate for all parameters", min_value=0.0001, max_value=1.00, value=0.005, step=0.0001, key='lr_all_svd'),
                "reg_all": st.sidebar.number_input("Regularization term for all parameters", min_value=0.0001, max_value=1.00, value=0.02, key='reg_all_svd')}
    if algorithm == "BaselineOnly":
        st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
        return {"bsl_options": {"method": st.sidebar.selectbox("Baseline method", ["als", "sgd"], key='method_baselineonly'),
                                "reg_i": st.sidebar.number_input("Regularization term for item parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_i_baselineonly'),
                                "reg_u": st.sidebar.number_input("Regularization term for user parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_u_baselineonly')}}
    if algorithm == "CoClustering":
        st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
        return {"n_cltr_u": st.sidebar.number_input("Number of clusters for users", min_value=1, max_value=1000, value=5),
                "n_cltr_i": st.sidebar.number_input("Number of clusters for items", min_value=1, max_value=1000, value=5)}
    if algorithm == "NMF":
        st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
        return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_nmf'),
                "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_nmf'),
                "reg_pu": st.sidebar.number_input("Regularization term for user factors", min_value=0.0001, max_value=1.0, value=0.02),
                "reg_qi": st.sidebar.number_input("Regularization term for item factors", min_value=0.0001, max_value=1.0, value=0.02)}
    if algorithm == "NormalPredictor":
        return {}
    if algorithm == "SlopeOne":
        return {}
    if algorithm == "SVDpp":
        st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
        return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_svdpp'),
                "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_svdpp'),
                "lr_all": st.sidebar.number_input("Learning rate for all parameters", min_value=0.0001, max_value=1.0, value=0.005, key='lr_all_svdpp'),
                "reg_all": st.sidebar.number_input("Regularization term for all parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_all_svdpp')}
    if algorithm == "KNNBasic":
        return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbasic'),
                "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["pearson", "msd", "cosine"], key='sim_options_knnbasic'),
                                "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnbasic')}}
    if algorithm == "KNNWithMeans":
        return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnwithmeans'),
                "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["pearson", "msd", "cosine"], key='sim_options_knnwithmeans'),
                                "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnwithmeans')}}
    if algorithm == "KNNWithZScore":
        return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnwithzscore'),
                "min_k": st.sidebar.number_input("Minimum number of nearest neighbors", min_value=1, max_value=1000, value=1, key='min_k_knnwithzscore'),
                "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["pearson", "msd", "cosine"], key='sim_options_knnwithzscore'),
                                "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnwithzscore')}}
    if algorithm == "KNNBaseline":
        return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbaseline'),
                "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["pearson", "msd", "cosine"], key='sim_options_knnbaseline'),
                                "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnbaseline')},
                "bsl_options": {"method": st.sidebar.selectbox("Baseline method", ["als", "sgd"], key='method_knnbaseline'),
                                "reg_i": st.sidebar.number_input("Regularization term for item parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_i_knnbaseline'),
                                "reg_u": st.sidebar.number_input("Regularization term for user parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_u_knnbaseline')}}

def evaluate_algo(algo_list, strategy_instance, metrics, data):
    """
    Evaluates recommendation algorithms.
    :param algo_list: Recommendation algorithms.
    :param strategy_instance: Split strategy.
    :param metrics: The evaluation metrics.
    :param data: Recommendation data.
    :return: A dataframe with evaluation results.
    """
    results = []
    # To count the number of folds for each algorithm:
    fold_counter = {}
    fold_count = 0
    with st.spinner("Evaluating algorithms..."):
        for algo in algo_list:
            fold_count += 1
            cross_validate_results = evaluation.cross_validate(algo, data, measures=metrics, cv=strategy_instance)
            for i in range(strategy_instance.n_splits):
                row = {}
                algo_name = type(algo).__name__
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
                results.append(row)
    df = pd.DataFrame(results)
    cols = ["Fold"] + [col for col in df.columns if col != "Fold"] # Move the "Fold" column to the first position
    df = df[cols]
    return df

def select_split_strategy(strategy):
    """
    Select parameters related to the specified split strategy (RS).
    :param strategy: The split strategy.
    :return: A dictionary with parameter values. 
    """
    if strategy == "KFold":
        st.sidebar.markdown("""A basic cross-validation iterator. Each fold is used once as a testset while the k - 1 remaining folds are used for training.""")
        return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
                "shuffle": st.sidebar.checkbox("Shuffle?")}
    elif strategy == "RepeatedKFold":
        st.sidebar.markdown("""Repeats KFold n times with different randomization in each repetition.""")
        return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
                "n_repeats": st.sidebar.number_input("Number of repeats", min_value=1, max_value=10, value=1)}
    elif strategy == "ShuffleSplit":
        st.sidebar.markdown("""A basic cross-validation iterator with random trainsets and testsets. Contrary to other cross-validation strategies, random splits do not guarantee that all folds will be different, although this is still very likely for sizeable datasets.""")
        return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
                "test_size": st.sidebar.number_input("Test size", min_value=0.1, max_value=0.9, step=0.1, value=0.2),
                "shuffle": st.sidebar.checkbox("Shuffle?")}
    elif strategy == "LeaveOneOut":
        st.sidebar.markdown("""Cross-validation iterator where each user has exactly one rating in the testset. Contrary to other cross-validation strategies, LeaveOneOut does not guarantee that all folds will be different, although this is still very likely for sizeable datasets.""")
        return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
                "min_n_ratings": st.sidebar.number_input("Minimum number of ratings for each user (trainset)", min_value=0, max_value=10000, value=0)}
    
def visualize_graph_mean_rs(df, increment_yaxis):
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

def visualize_graph_fold_rs(df, metric, increment_yaxis):
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
    