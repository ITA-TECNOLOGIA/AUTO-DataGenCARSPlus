import pandas as pd
import plotly.graph_objs as go
import streamlit as st
from datagencars.evaluation import sklearn_helpers
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util


def evaluate_cm_paradigm(rating_df):
    """
    Evaluates the contextual modeling paradigm.
    :param rating_df: The rating dataframe.
    :param item_df: The item dataframe to extract candidate features (item attributtes) of the classifier.
    :param context_df: The context dataframe to extract candidate features (context attributtes) of the classifier.
    """
    # Building the knowledge base:    
    knowledge_base_df = build_knowledge_base(rating_df)
        
    # Selecting and building classification algorithms:    
    classifier_list = select_classification_algorithm()

    # Selecting the split strategy:
    split_strategy, split_strategy_parameter_dict = select_split_strategy()
    split_strategy_instance = sklearn_helpers.create_split_strategy(strategy=split_strategy, strategy_params=split_strategy_parameter_dict)

    # Selecting evaluation metrics:
    metric_list = select_evaluation_metric()

    # Evaluating classification algorithm:
    evaluation_result_df, selected_users = evaluate(knowledge_base_df, classifier_list, split_strategy_instance, metric_list)
    
    # Showing evaluation results:
    show_evaluation_result(evaluation_result_df, selected_users)
      
def build_knowledge_base(rating_df):
    """
    Builds the knowledge base to the classifier will be used in contextual modeling paradigm.
    :param rating_df: The rating dataframe.
    :return: A dataframe with the knowledge base.
    """    
    # Loading item and context files:
    st.markdown("""---""")
    st.markdown('**Knowledge base:**')
    st.write('If you are applying the Contextual Modeling paradigm, upload the following files to select the features of the knowledge base: ')
    item_df = wf_util.load_one_file(file_type=config.ITEM_TYPE, wf_type='evaluation_cars_item_df') 
    context_df = wf_util.load_one_file(file_type=config.CONTEXT_TYPE, wf_type='evaluation_cars_context_df')
    # Building the knowledge base:
    knowledge_base_df = pd.DataFrame()
    if (not item_df.empty) and (not context_df.empty):
        st.sidebar.markdown("""---""")
        st.sidebar.markdown('**Contextual features selection**')
        # Selecting contextual features:
        item_feature_df = select_contextual_features(df=item_df, label=config.ITEM_TYPE)                    
        context_feature_df = select_contextual_features(df=context_df, label=config.CONTEXT_TYPE)
        # Merging rating_df, item_df and context_id dataframes:
        if 'context_id' not in rating_df.columns:
            st.error(f'The uploaded {config.RATING_TYPE} file must contain contextual information (context_id).')
        else:
            if not item_feature_df.empty:
                knowledge_base_df = rating_df.merge(item_feature_df, on='item_id')
            if not context_feature_df.empty:
                knowledge_base_df = knowledge_base_df.merge(context_feature_df, on='context_id')
            knowledge_base_df.drop('context_id', axis=1, inplace=True)
            # Column name you want to move to the last position
            column_name_to_move = 'rating'
            # Create a new DataFrame with the desired column at the end
            new_rating_column_order = [col for col in knowledge_base_df.columns if col != column_name_to_move] + [column_name_to_move]
            knowledge_base_df = knowledge_base_df[new_rating_column_order]         
            print('The knowledge base has been built.')   
        # Showing the knowledge base built:
        with st.expander(label='Show the knowledge base built'):
            st.dataframe(knowledge_base_df)
    else:
        st.warning("The item and context files have not been uploaded.")
    return knowledge_base_df

def select_contextual_features(df, label):
    """
    Gets a sub-dataframe with the user-selected item or context features (from item_df or context_df, respectively).
    :param df: The item or context dataframe.
    :param label: The item or context label ("item" or "context").
    ;return: A sub-dataframe with the user-selected item or context features.
    """
    # Excluding the item_id or context_id:
    column_names = df.columns[1:].tolist()
    selected_columns = st.sidebar.multiselect(label=f'Select {label} features:', options=column_names, default=column_names)
    if selected_columns:
        return df[[label+'_id']+selected_columns]
    else:
        return pd.DataFrame()
    
def select_classification_algorithm():
    """
    Selects a classification algorithm.

    """
    st.sidebar.markdown("""---""")
    st.sidebar.markdown('**Classifier selection**')
    st.sidebar.write("-0.5 values will be replaced with None") # why?

    # Selecting classifiers to evaluate:
    st.markdown("""---""")
    st.markdown('**Classification algoritms:**')
    classifier_name_list = st.sidebar.multiselect("Select one or more classifiers", config.CLASSIFIER_OPTIONS, default=config.CLASSIFIER_OPTIONS[0])
    # Replacing some values and building classifiers.
    classifier_list = []
    # Help information:
    help_information.help_classification_algoritms(classifier_name_list)            
    # Parameter settings:
    for classifier_name in classifier_name_list:
        # Selecting classification parameters:
        classification_parameters_map = select_classification_parameters_map(classification_algorithm=classifier_name)
        # Replacing -0.5 values by NaN values:
        replaced_classification_parameters_map = replace_with_none_values(classification_parameters_map)                
        # Built classifier:                            
        classifier_instance = sklearn_helpers.create_algorithm(classifier_name, replaced_classification_parameters_map)
        classifier_list.append(classifier_instance)
    print(f'The classification algorithm {classifier_list} have been selected.')
    st.sidebar.markdown("""---""")
    return classifier_list

def replace_with_none_values(classification_parameters_map):
    """
    Replaces -0.5 values by NaN values.
    :param classification_parameters_map: TODO
    :return: TODO
    """
    for key, value in classification_parameters_map.items():
        if value == -0.5:
            classification_parameters_map[key] = None
    return classification_parameters_map

def select_classification_parameters_map(classification_algorithm):
    """
    Select parameters of the specified classification algorithm.
    :param classification_algorithm: The classification algorithm.
    :return: A dictionary with parameter values.
    """
    if classification_algorithm == "KNeighborsClassifier":
        return {"n_neighbors": st.sidebar.number_input("Number of neighbors", min_value=1, max_value=1000, value=5, key='n_neighbors_kneighborsclassifier'),
                "weights": st.sidebar.selectbox("Weights", ["uniform", "distance"], key='weights_kneighborsclassifier'),
                "algorithm": st.sidebar.selectbox("Algorithm", ["auto", "ball_tree", "kd_tree", "brute"], key='algorithm_kneighborsclassifier'),
                "leaf_size": st.sidebar.number_input("Leaf size", min_value=1, max_value=1000, value=30, key='leaf_size_kneighborsclassifier'),
                "p": st.sidebar.number_input("P", min_value=1, max_value=1000, value=2, key='p_kneighborsclassifier'),
                "metric": st.sidebar.selectbox("Metric", ["minkowski", "euclidean", "manhattan", "chebyshev", "seuclidean", "mahalanobis", "wminkowski", "haversine"], key='metric_kneighborsclassifier'),
                "n_jobs": st.sidebar.number_input("Number of jobs", min_value=1, max_value=1000, value=1, key='n_jobs_kneighborsclassifier')}
    elif classification_algorithm == "SVC":
        return {"C": st.sidebar.number_input("C", min_value=0.0001, max_value=1000.0, value=1.0, key='C_svc'),
                "kernel": st.sidebar.selectbox("Kernel", ["linear", "poly", "rbf", "sigmoid", "precomputed"], key='kernel_svc'),
                "degree": st.sidebar.number_input("Degree", min_value=1, max_value=1000, value=3, key='degree_svc'),
                "gamma": st.sidebar.selectbox("Gamma", ["scale", "auto"], key='gamma_svc'),
                "coef0": st.sidebar.number_input("Coef0", min_value=0.0, max_value=1000.0, value=0.0, key='coef0_svc'),
                "shrinking": st.sidebar.checkbox("Shrinking?", key='shrinking_svc'),
                "probability": st.sidebar.checkbox("Probability?", key='probability_svc'),
                "tol": st.sidebar.number_input("Tol", min_value=0.0001, max_value=1000.0, value=0.001, key='tol_svc'),
                "cache_size": st.sidebar.number_input("Cache size", min_value=0.0001, max_value=1000.0000, value=200.0000, key='cache_size_svc'),
                "class_weight": st.sidebar.selectbox("Class weight", ["balanced", None], key='class_weight_svc'),
                "verbose": st.sidebar.checkbox("Verbose?", key='verbose_svc'),
                "max_iter": st.sidebar.number_input("Maximum iterations", min_value=-1, max_value=1000, value=-1, key='max_iter_svc'),
                "decision_function_shape": st.sidebar.selectbox("Decision function shape", ["ovo", "ovr"], key='decision_function_shape_svc'),
                "random_state": st.sidebar.number_input("Random state", min_value=-0.5, max_value=1000.0, value=-0.5, key='random_state_svc'),
                "break_ties": st.sidebar.checkbox("Break ties?", key='break_ties_svc')}
    elif classification_algorithm == "GaussianNB":
        return {}
    elif classification_algorithm == "RandomForestClassifier":
        return {"n_estimators": st.sidebar.number_input("Number of estimators", min_value=1, max_value=1000, value=100, key='n_estimators_randomforestclassifier'),
                "criterion": st.sidebar.selectbox("Criterion", ["gini", "entropy"], key='criterion_randomforestclassifier'),
                "max_depth": st.sidebar.number_input("Maximum depth", min_value=-0.5, max_value=1000.0, value=-0.5, key='max_depth_randomforestclassifier'),
                "min_samples_split": st.sidebar.number_input("Minimum samples split", min_value=1, max_value=1000, value=2, key='min_samples_split_randomforestclassifier'),
                "min_samples_leaf": st.sidebar.number_input("Minimum samples leaf", min_value=1, max_value=1000, value=1, key='min_samples_leaf_randomforestclassifier'),
                "min_weight_fraction_leaf": st.sidebar.number_input("Minimum weight fraction leaf", min_value=0.0001, max_value=1.0, value=0.01, key='min_weight_fraction_leaf_randomforestclassifier'),
                "max_features": st.sidebar.selectbox("Maximum features", ["auto", "sqrt", "log2", None], key='max_features_randomforestclassifier'),
                "max_leaf_nodes": st.sidebar.number_input("Maximum leaf nodes", min_value=-0.5, max_value=1000.0, value=-0.5, key='max_leaf_nodes_randomforestclassifier'),
                "min_impurity_decrease": st.sidebar.number_input("Minimum impurity decrease", min_value=0.0001, max_value=1.0, value=0.01, key='min_impurity_decrease_randomforestclassifier'),
                "bootstrap": st.sidebar.checkbox("Bootstrap?", key='bootstrap_randomforestclassifier'),
                "oob_score": st.sidebar.checkbox("OOB score?", key='oob_score_randomforestclassifier'),
                "n_jobs": st.sidebar.number_input("Number of jobs", min_value=-0.5, max_value=1000.0, value=-0.5, key='n_jobs_randomforestclassifier'),
                "random_state": st.sidebar.number_input("Random state", min_value=-0.5, max_value=1000.0, value=-0.5, key='random_state_randomforestclassifier'),
                "verbose": st.sidebar.number_input("Verbose", min_value=0, max_value=1000, value=0, key='verbose_randomforestclassifier'),
                "ccp_alpha": st.sidebar.number_input("CCP alpha", min_value=0.0001, max_value=1.0, value=0.01, key='ccp_alpha_randomforestclassifier'),
                "class_weight": st.sidebar.selectbox("Class weight", ["balanced", "balanced_subsample", None], key='class_weight_randomforestclassifier'),
                "max_samples": st.sidebar.number_input("Maximum samples", min_value=-0.5, max_value=1.0, value=-0.5, key='max_samples_randomforestclassifier'),
                "warm_start": st.sidebar.checkbox("Warm start?", key='warm_start_randomforestclassifier')}
    elif classification_algorithm == "KMeans":
        return {"n_clusters": st.sidebar.number_input("Number of clusters", min_value=1, max_value=1000, value=5, key='n_clusters_kmeans'),
                "init": st.sidebar.selectbox("Initialization method", ["k-means++", "random"], key='init_kmeans'),
                "n_init": st.sidebar.number_input("Number of initializations", min_value=1, max_value=1000, value=10, key='n_init_kmeans'),
                "max_iter": st.sidebar.number_input("Maximum number of iterations", min_value=1, max_value=1000, value=300, key='max_iter_kmeans'),
                "tol": st.sidebar.number_input("Tolerance", min_value=0.0001, max_value=1.0, value=0.0001, key='tol_kmeans')}
    elif classification_algorithm == "HistGradientBoostingClassifier":
        return {"learning_rate": st.sidebar.slider("Learning rate", 0.01, 1.0, 0.1, step=0.01),
                "max_iter": st.sidebar.slider("Max number of iterations", 10, 1000, 100, step=10),
                "max_leaf_nodes": st.sidebar.slider("Max leaf nodes", 10, 200, 31, step=1),
                "max_depth": st.sidebar.slider("Max depth", 1, 50, 15, step=1),
                "l2_regularization": st.sidebar.slider("L2 regularization", 0.0, 1.0, 0.0, step=0.01)}
    
def select_split_strategy():
    """
    Selects split strategies (ShuffleSplit, KFold or LeaveOneOut) to evaluate classification algorithm.
    :return: A dictionary with parameter values. 
    """
    st.sidebar.markdown('**Split strategy selection**')
    split_strategy = st.sidebar.selectbox("Select a strategy", ["KFold", "ShuffleSplit", "LeaveOneOut"]) # , "PredefinedKFold", "train_test_split", "RepeatedKFold",
    split_strategy_parameter_dict = {}
    if split_strategy == "ShuffleSplit":
        n_splits = st.sidebar.number_input("Number of splits", 2, 100, 10)
        train_size = st.sidebar.slider("Train set size (0.0 to 1.0)", 0.01, 1.0, 0.2, step=0.01)
        split_strategy_parameter_dict = {"n_splits": n_splits, "train_size": train_size}
    elif split_strategy == "KFold":
        n_splits = st.sidebar.number_input("Number of folds", 2, 100, 5)
        split_strategy_parameter_dict = {"n_splits": n_splits, "shuffle": st.sidebar.checkbox("Shuffle?")}
    elif split_strategy == "LeaveOneOut":
        st.sidebar.markdown("""Cross-validation iterator where each user has exactly one rating in the testset. Contrary to other cross-validation strategies, LeaveOneOut does not guarantee that all folds will be different, although this is still very likely for sizeable datasets.""")
        split_strategy_parameter_dict = {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
                                   "min_n_ratings": st.sidebar.number_input("Minimum number of ratings for each user (trainset)", min_value=0, max_value=10000, value=0)}            
    print(f'The split strategy ({split_strategy}) has been selected.')
    return split_strategy, split_strategy_parameter_dict

def select_evaluation_metric():  
    """
    Selects evaluation metrics.
    :return: A list with the evaluation metrics.
    """  
    st.sidebar.markdown('**Metrics selection**')  
    metric_list = st.sidebar.multiselect("Select one or more metrics", config.SCIKIT_LEARN_METRICS, default="Precision")
    print(f'The evaluation metrics ({metric_list}) have been selected.')
    st.sidebar.markdown("""---""")
    return metric_list

def evaluate(knowledge_base_df, classifier_list, split_strategy_instance, metric_list):
    """
    Evaluation a classification algorithm.
    :param knowledge_base_df: The knowledge base.
    :param classifier_list: The list of classifiers to evaluate.
    :param split_strategy_instance: A object of the split strategy to use during the evaluation.
    :param metric_list: The list of metrics to use during the evaluation.
    :return: A dataframe with evaluation results.
    """
    st.sidebar.markdown('**Target user**')
    evaluation_result_df = pd.DataFrame()
    selected_users = []
    if not knowledge_base_df.empty:
        # Extract unique user_ids and add "All users" option:
        user_ids = sorted(knowledge_base_df['user_id'].unique().tolist())
        user_options = ["All users"] + user_ids
        selected_users = st.sidebar.multiselect("Select one or more users or 'All users'", options=user_options, default="All users")
        if st.sidebar.button("Evaluate"):
            if "All users" in selected_users:
                target_user_ids = None
            else:
                target_user_ids = selected_users                            
            evaluation_result_df = sklearn_helpers.evaluate(knowledge_base_df, classifier_list, split_strategy_instance, metric_list, target_user_ids)
            # Save the results dataframe in the session state:
            st.session_state["evaluation_result_df"] = evaluation_result_df
            print('The contextual modeling paradigm has been evaluated.')
    return evaluation_result_df, selected_users

def show_evaluation_result(evaluation_result_df, selected_users):
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
        metric_list = evaluation_result_df.columns[3:].tolist()                 
        mean_results_df = evaluation_result_df.groupby(['User','Algorithm'])[metric_list].mean().reset_index()
        # Showing result dataframe by mean:
        st.dataframe(mean_results_df)    
        # Save dataframe:                
        wf_util.save_df(df_name='mean_evaluation_results', df_value=mean_results_df, extension='csv') 
        
        # Evaluation figures:
        st.subheader("Evaluation graphs (folds and means)")
        with_fold = st.selectbox(label="Select one option to plot", options=['Means', 'Folds']) 
        col_algorithm, col_metric, col_user = st.columns(3)
        with col_algorithm:
            algorithm_list = evaluation_result_df["Algorithm"].unique().tolist()
            st.session_state['selected_algorithm_list'] = st.multiselect(label="Select an algorithm", options=algorithm_list, default=algorithm_list)
        with col_metric:                            
            st.session_state['selected_metric_list'] = st.multiselect(label="Select a metric", options=metric_list, default=metric_list)
        with col_user:                                                
            
            # user_list = evaluation_result_df["User"].unique().tolist()
            st.session_state['selected_users_list'] = st.multiselect(label="Select a user", options=selected_users, default=selected_users)  
        # Increasing the maximum value of the Y-axis:
        increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
        # Plotting the graph (by using the "Means" option):
        if with_fold == 'Means':                             
            # Showing graph:               
            if st.button(label='Show graph'):
                draw_graph_by_mean(evaluation_result_df, st.session_state['selected_algorithm_list'], st.session_state['selected_metric_list'], st.session_state['selected_users_list'], increment_yaxis)
                # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
                df = mean_results_df.loc[mean_results_df['Algorithm'].isin(st.session_state['selected_algorithm_list']), ['User', 'Algorithm']+st.session_state['selected_metric_list']]
                with st.expander(label='Data to plot in the graphic'):
                    st.dataframe(df)
        elif with_fold == 'Folds': # Plotting the graph (by using the "Folds" option):                            
            # Showing graph:               
            if st.button(label='Show graph'):                                
                draw_graph_by_fold(evaluation_result_df, st.session_state['selected_algorithm_list'], st.session_state['selected_metric_list'], st.session_state['selected_users_list'], increment_yaxis)
                # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:                                
                df = evaluation_result_df.loc[evaluation_result_df['Algorithm'].isin(st.session_state['selected_algorithm_list']), ['User', 'Fold', 'Algorithm']+st.session_state['selected_metric_list']]
                with st.expander(label='Data to plot in the graphic'):
                    st.dataframe(df)

def draw_graph_by_mean(df, algorithms, metrics, selected_users, increment_yaxis):
    """
    Visualize a bar graphic with evaluation results considering different algorithms, metrics and users.
    :param df: A dataframe with evaluation results.
    :param algorithms: List of recommendation algorithms.
    :param metrics: List of metrics.
    :param selected_users: List of users.
    """
    fig = go.Figure()
    for algorithm in algorithms:
        filtered_df = df[df["Algorithm"] == algorithm]
        for metric in metrics:
            if "All users" in selected_users:
                users = df["User"].unique()
                user_label = "All users"
                user_filtered_df = filtered_df[filtered_df["User"].isin(users)]
                mean_value = user_filtered_df[metric].mean()
                fig.add_trace(go.Bar(x=[f"{metric}"], y=[mean_value], name=f"{algorithm} - {user_label}", legendgroup=f"{algorithm} - {user_label}"))
            else:
                for user in selected_users:
                    user_filtered_df = filtered_df[filtered_df["User"] == user]
                    mean_value = user_filtered_df[metric].mean()
                    fig.add_trace(go.Bar(x=[f"{metric}"], y=[mean_value], name=f"{algorithm} - User {user}", legendgroup=f"{algorithm} - User {user}"))
    fig.update_layout(xaxis_title="Measures of performance", yaxis_title="Performance", legend=dict(title="Algorithms & Users"), barmode='group', yaxis_range=[0, df[metrics].max().max()+increment_yaxis])
    st.plotly_chart(fig, use_container_width=True)

def draw_graph_by_fold(df, algorithms, metrics, selected_users, increment_yaxis):
    """
    Visualize a line graphic with evaluation results considering different algorithms, metrics and users.
    :param df: A dataframe with evaluation results.
    :param algorithms: List of recommendation algorithms.
    :param metrics: List of metrics.
    :param selected_users: List of users.
    """
    filtered_df = df[df["Algorithm"].isin(algorithms)]
    fig = go.Figure()
    for algorithm in algorithms:
        for metric in metrics:
            if "All users" in selected_users:
                users = df["User"].unique()
                algo_filtered_df = filtered_df[(filtered_df["Algorithm"] == algorithm) & (filtered_df["User"].isin(users))]
                mean_values = []
                for fold in algo_filtered_df["Fold"].unique():
                    fold_filtered_df = algo_filtered_df[algo_filtered_df["Fold"] == fold]
                    mean_value = fold_filtered_df[metric].mean()
                    mean_values.append(mean_value)
                fig.add_trace(go.Scatter(x=algo_filtered_df["Fold"].unique(), y=mean_values, name=f"{algorithm} - {metric} - All users", mode="markers+lines"))
            else:
                for user in selected_users:
                    algo_user_filtered_df = filtered_df[(filtered_df["Algorithm"] == algorithm) & (filtered_df["User"] == user)]
                    fig.add_trace(go.Scatter(x=algo_user_filtered_df["Fold"], y=algo_user_filtered_df[metric], name=f"{algorithm} - {metric} - User {user}", mode="markers+lines"))
    fig.update_layout(xaxis=dict(title="Fold", dtick=1, tickmode='linear'), yaxis_title="Performance", legend=dict(title="Measures of performance"), yaxis_range=[0, df[metrics].max().max()+increment_yaxis])
    st.plotly_chart(fig, use_container_width=True)
