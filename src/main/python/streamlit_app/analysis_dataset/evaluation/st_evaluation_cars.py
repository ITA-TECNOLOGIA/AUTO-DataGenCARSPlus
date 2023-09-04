import streamlit as st
from streamlit_app import config, help_information
from streamlit_app.preprocess_dataset import wf_util
from datagencars.evaluation import sklearn_helpers


def evaluate():
    """
    Evaluating Context-Aware Recommendation Systems.
    """
    st.header('Evaluation of CARS')

    # Loading rating file:
    user_df, item_df, context_df, rating_df, __ = wf_util.load_dataset(file_type_list=config.DATASET_CARS, wf_type='evaluation_cars')
    st.sidebar.markdown("""---""")

    if (not rating_df.empty) and (not item_df.empty) and (not context_df.empty):
        st.sidebar.markdown("""---""")
        # SELECTING PARADIGM TO EVALUATE:
        st.sidebar.markdown('**CARS paradigm selection**')
        paradigm = st.sidebar.selectbox("Select one paradigm", ["Contextual Modeling", "Pre-filtering", "Post-filtering"])
        lars = st.sidebar.checkbox('LARS', value=True)
        st.session_state["lars"] = lars
        if lars:
            side_lars = st.sidebar.checkbox('SocIal-Distance prEserving', value=True)
            st.session_state["side_lars"] = side_lars
        st.sidebar.markdown("""---""")
        if paradigm == "Contextual Modeling":
            # SELECTING CONTEXTUAL FEATURES:
            st.sidebar.markdown('**Contextual features selection**')
            item_feature_df = select_contextual_features(df=item_df, label="item")                    
            context_feature_df = select_contextual_features(df=context_df, label="context")
            # Building knowledge base:                    
            try:
                merged_df = rating_df.merge(item_feature_df, on='item_id').merge(context_feature_df, on='context_id')
                merged_df.drop('context_id', axis=1, inplace=True)
            except KeyError as e:
                st.error(f"The rating, user, item and context datasets do not have '_id' columns in common. {e}")                    
            st.sidebar.markdown("""---""")
            # SELECTING CLASSIFIER:
            st.sidebar.markdown('**Classifier selection**')
            classifier_name_list = st.sidebar.multiselect("Select one or more classifiers", ["KNeighborsClassifier", "SVC", "GaussianNB", "RandomForestClassifier", "KMeans", "HistGradientBoostingClassifier"], default="KNeighborsClassifier")
            # Replacing some values and building classifiers.
            classifier_list = []
            st.sidebar.write("-0.5 values will be replaced with None")
            # Help information:
            help_information.help_classification_algoritms(classifier_name_list)            
            for classifier_name in classifier_name_list:
                classifier_params = replace_with_none(select_params_contextual(classifier_name))                
                # PARAMETER SETTINGS:                            
                classifier_instance = sklearn_helpers.create_algorithm(classifier_name, classifier_params)
                classifier_list.append(classifier_instance)
                st.sidebar.markdown("""---""")
            
            # CROSS VALIDATION:
            st.sidebar.markdown('**Split strategy selection**')
            strategy = st.sidebar.selectbox("Select a strategy", ["KFold", "ShuffleSplit", "LeaveOneOut"]) # , "PredefinedKFold", "train_test_split", "RepeatedKFold", 
            strategy_params = select_split_strategy_contextual(strategy)
            strategy_instance = sklearn_helpers.create_split_strategy(strategy, strategy_params)
            st.sidebar.markdown("""---""")
            
            # METRICS:
            st.sidebar.markdown('**Metrics selection**')  
            metrics = st.sidebar.multiselect("Select one or more metrics", config.SCIKIT_LEARN_METRICS, default="Precision")
            st.sidebar.markdown("""---""")
            
            # EVALUATION:
            st.sidebar.markdown('**Target user**')
            # Extract unique user_ids and add "All users" option
            user_ids = sorted(rating_df['user_id'].unique().tolist())
            user_options = ["All users"] + user_ids
            selected_users = st.sidebar.multiselect("Select one or more users or 'All users'", options=user_options, default="All users")
            if st.sidebar.button("Evaluate"):
                if "All users" in selected_users:
                    target_user_ids = None
                else:
                    target_user_ids = selected_users                            
                fold_results_df = sklearn_helpers.evaluate(merged_df, classifier_list, strategy_instance, metrics, target_user_ids)
                st.session_state["fold_results"] = fold_results_df #Save the results dataframe in the session state
            
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
                metric_list = fold_results_df.columns[3:].tolist()                 
                mean_results_df = fold_results_df.groupby(['User','Algorithm'])[metric_list].mean().reset_index()
                # Showing result dataframe by mean:
                st.dataframe(mean_results_df)    
                # Save dataframe:                
                wf_util.save_df(df_name='mean_evaluation_results', df_value=mean_results_df, extension='csv') 
                
                # Evaluation figures:
                st.subheader("Evaluation graphs (folds and means)")
                with_fold = st.selectbox(label="Select one option to plot", options=['Means', 'Folds']) 
                col_algorithm, col_metric, col_user = st.columns(3)
                with col_algorithm:
                    st.session_state['selected_algorithm_list'] = st.multiselect(label="Select an algorithm", options=fold_results_df["Algorithm"].unique().tolist())
                with col_metric:                            
                    st.session_state['selected_metric_list'] = st.multiselect(label="Select a metric", options=metric_list)
                with col_user:                                                        
                    st.session_state['selected_users_list'] = st.multiselect(label="Select a user", options=selected_users)  
                # Increasing the maximum value of the Y-axis:
                increment_yaxis = st.number_input("How to increment the maximum value of the Y-axis", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
                # Plotting the graph (by using the "Means" option):
                if with_fold == 'Means':                             
                    # Showing graph:               
                    if st.button(label='Show graph'):
                        visualize_graph_mean_cars(fold_results_df, st.session_state['selected_algorithm_list'], st.session_state['selected_metric_list'], st.session_state['selected_users_list'], increment_yaxis)
                        # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:
                        df = mean_results_df.loc[mean_results_df['Algorithm'].isin(st.session_state['selected_algorithm_list']), ['User', 'Algorithm']+st.session_state['selected_metric_list']]
                        with st.expander(label='Data to plot in the graphic'):
                            st.dataframe(df)
                elif with_fold == 'Folds': # Plotting the graph (by using the "Folds" option):                            
                    # Showing graph:               
                    if st.button(label='Show graph'):                                
                        visualize_graph_fold_cars(fold_results_df, st.session_state['selected_algorithm_list'], st.session_state['selected_metric_list'], st.session_state['selected_users_list'], increment_yaxis)
                        # Filtering the dataframe (with means) by the algorithms and metrics selected by the user:                                
                        df = fold_results_df.loc[fold_results_df['Algorithm'].isin(st.session_state['selected_algorithm_list']), ['User', 'Fold', 'Algorithm']+st.session_state['selected_metric_list']]
                        with st.expander(label='Data to plot in the graphic'):
                            st.dataframe(df)
        elif paradigm == "Post-filtering":
            if side_lars and (not user_df.empty) and (not item_df.empty) and (not context_df.empty) and (not rating_df.empty) and (not behavior_df.empty):
                st.sidebar.header("Algorithm selection")
                algorithms = st.sidebar.multiselect("Select one or more algorithms", ["KNNBasic", "KNNWithMeans", "KNNWithZScore", "KNNBaseline"], default="KNNBasic")
                algo_list = []
                for algorithm in algorithms:
                    algo_params = select_params(algorithm)
                    algo_instance = surprise_helpers.create_algorithm(algorithm, algo_params)
                    algo_list.append(algo_instance)
                    st.sidebar.markdown("""---""")
                st.sidebar.header("Split strategy selection")
                strategy = st.sidebar.selectbox("Select a strategy", ["KFold", "RepeatedKFold", "ShuffleSplit", "LeaveOneOut", "PredefinedKFold", "train_test_split"])
                strategy_params = util.select_split_strategy(strategy)
                strategy_instance = surprise_helpers.create_split_strategy(strategy, strategy_params)
                data = surprise_helpers.convert_to_surprise_dataset(rating_df)
                st.sidebar.header("Metrics selection")
                if binary_ratings.is_binary_rating(rating_df):
                    metrics = st.sidebar.multiselect("Select one or more cross validation binary metrics", ["Precision", "Recall", "F1_Score", "AUC_ROC"], default="Precision")
                else:
                    metrics = st.sidebar.multiselect("Select one or more cross validation non-binary metrics", ["RMSE", "MSE", "MAE", "FCP", "Precision", "Recall", "F1_Score", "MAP", "NDCG"], default="MAE")
                # EVALUATION:
                if st.sidebar.button("Evaluate"):
                    fold_results_df = util.evaluate_algo(algo_list, strategy_instance, metrics, data)
                    st.session_state["fold_results"] = fold_results_df #Save the results dataframe in the session state
                # RESULTS:
                if "fold_results" in st.session_state:
                    # Results (folds):
                    fold_results_df = st.session_state["fold_results"]
                    st.subheader("Detailed evaluation results (folds and means)")
                    st.dataframe(fold_results_df)                    
                    link_fold_result = f'<a href="data:file/csv;base64,{base64.b64encode(fold_results_df.to_csv(index=False).encode()).decode()}" download="fold_evaluation_results.csv">Download results</a>'
                    st.markdown(link_fold_result, unsafe_allow_html=True)
                    # Results (means):
                    metric_list = fold_results_df.columns[2:].tolist()
                    mean_results_df = fold_results_df.groupby('Algorithm')[metric_list].mean().reset_index()
                    st.dataframe(mean_results_df)                    
                    link_mean_result = f'<a href="data:file/csv;base64,{base64.b64encode(mean_results_df.to_csv(index=False).encode()).decode()}" download="mean_evaluation_results.csv">Download results</a>'
                    st.markdown(link_mean_result, unsafe_allow_html=True)
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
                            util.visualize_graph_mean_rs(df, increment_yaxis)
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
                            util.visualize_graph_fold_rs(df, selected_metric, increment_yaxis)
                            with st.expander(label='Data to plot in the graphic'):
                                st.dataframe(df)
            else:
                st.error(st.warning("The user, item, context, rating and behavior files have not been uploaded."))
        else:
            st.write("TODO: pre-filtering")
    else:
        st.warning("The item, context and rating files have not been uploaded.")

def select_contextual_features(df, label):
    """
    Gets a sub-dataframe with the user-selected item or context features (from item_df or context_df, respectively).
    :param df: The item or context dataframe.
    :param label: The item or context label ("item" or "context").
    ;return: A sub-dataframe with the user-selected item or context features.
    """
    column_names = df.columns[1:].tolist() # Excluding the item_id or context_id.    
    selected_columns = st.sidebar.multiselect(label=f'Select {label} features:', options=column_names, default=column_names)
    if selected_columns:
        return df[[label+'_id']+selected_columns]
    
def replace_with_none(params):
    """
    TODO
    :param params: TODO
    :return: TODO
    """
    for key, value in params.items():
        if value == -0.5:
            params[key] = None
    return params

def select_params_contextual(algorithm):
    """
    Select parameters of the specified context-aware recommendation algorithm.
    :param algorithm: A context-aware recommendation algorithm.
    :return: A dictionary with parameter values.
    """
    if algorithm == "KNeighborsClassifier":
        return {"n_neighbors": st.sidebar.number_input("Number of neighbors", min_value=1, max_value=1000, value=5, key='n_neighbors_kneighborsclassifier'),
                "weights": st.sidebar.selectbox("Weights", ["uniform", "distance"], key='weights_kneighborsclassifier'),
                "algorithm": st.sidebar.selectbox("Algorithm", ["auto", "ball_tree", "kd_tree", "brute"], key='algorithm_kneighborsclassifier'),
                "leaf_size": st.sidebar.number_input("Leaf size", min_value=1, max_value=1000, value=30, key='leaf_size_kneighborsclassifier'),
                "p": st.sidebar.number_input("P", min_value=1, max_value=1000, value=2, key='p_kneighborsclassifier'),
                "metric": st.sidebar.selectbox("Metric", ["minkowski", "euclidean", "manhattan", "chebyshev", "seuclidean", "mahalanobis", "wminkowski", "haversine"], key='metric_kneighborsclassifier'),
                "n_jobs": st.sidebar.number_input("Number of jobs", min_value=1, max_value=1000, value=1, key='n_jobs_kneighborsclassifier')}
    elif algorithm == "SVC":
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
    elif algorithm == "GaussianNB":
        return {}
    elif algorithm == "RandomForestClassifier":
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
    elif algorithm == "KMeans":
        return {"n_clusters": st.sidebar.number_input("Number of clusters", min_value=1, max_value=1000, value=5, key='n_clusters_kmeans'),
                "init": st.sidebar.selectbox("Initialization method", ["k-means++", "random"], key='init_kmeans'),
                "n_init": st.sidebar.number_input("Number of initializations", min_value=1, max_value=1000, value=10, key='n_init_kmeans'),
                "max_iter": st.sidebar.number_input("Maximum number of iterations", min_value=1, max_value=1000, value=300, key='max_iter_kmeans'),
                "tol": st.sidebar.number_input("Tolerance", min_value=0.0001, max_value=1.0, value=0.0001, key='tol_kmeans')}
    elif algorithm == "HistGradientBoostingClassifier":
        return {"learning_rate": st.sidebar.slider("Learning rate", 0.01, 1.0, 0.1, step=0.01),
                "max_iter": st.sidebar.slider("Max number of iterations", 10, 1000, 100, step=10),
                "max_leaf_nodes": st.sidebar.slider("Max leaf nodes", 10, 200, 31, step=1),
                "max_depth": st.sidebar.slider("Max depth", 1, 50, 15, step=1),
                "l2_regularization": st.sidebar.slider("L2 regularization", 0.0, 1.0, 0.0, step=0.01)}
    
def select_split_strategy_contextual(strategy):
    """
    Select parameters related to the specified split strategy (CARS).
    :param strategy: The split strategy.
    :return: A dictionary with parameter values. 
    """
    if strategy == "ShuffleSplit":
        n_splits = st.sidebar.number_input("Number of splits", 2, 100, 10)
        train_size = st.sidebar.slider("Train set size (0.0 to 1.0)", 0.01, 1.0, 0.2, step=0.01)        
        return {"n_splits": n_splits, "train_size": train_size}
    elif strategy == "KFold":
        n_splits = st.sidebar.number_input("Number of folds", 2, 100, 5)             
        return {"n_splits": n_splits, "shuffle": st.sidebar.checkbox("Shuffle?")}
    elif strategy == "LeaveOneOut":
        st.sidebar.markdown("""Cross-validation iterator where each user has exactly one rating in the testset. Contrary to other cross-validation strategies, LeaveOneOut does not guarantee that all folds will be different, although this is still very likely for sizeable datasets.""")
        return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
                "min_n_ratings": st.sidebar.number_input("Minimum number of ratings for each user (trainset)", min_value=0, max_value=10000, value=0)}
    
def visualize_graph_mean_cars(df, algorithms, metrics, selected_users, increment_yaxis):
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
                fig.add_trace(go.Bar(
                    x=[f"{metric}"],
                    y=[mean_value],
                    name=f"{algorithm} - {user_label}",
                    legendgroup=f"{algorithm} - {user_label}"
                ))
            else:
                for user in selected_users:
                    user_filtered_df = filtered_df[filtered_df["User"] == user]
                    mean_value = user_filtered_df[metric].mean()
                    fig.add_trace(go.Bar(
                        x=[f"{metric}"],
                        y=[mean_value],
                        name=f"{algorithm} - User {user}",
                        legendgroup=f"{algorithm} - User {user}"
                    ))
    fig.update_layout(
        xaxis_title="Measures of performance",
        yaxis_title="Performance",
        legend=dict(title="Algorithms & Users"),
        barmode='group',
        yaxis_range=[0, df[metrics].max().max()+increment_yaxis]
    )
    st.plotly_chart(fig, use_container_width=True)

def visualize_graph_fold_cars(df, algorithms, metrics, selected_users, increment_yaxis):
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
                fig.add_trace(go.Scatter(
                    x=algo_filtered_df["Fold"].unique(),
                    y=mean_values,
                    name=f"{algorithm} - {metric} - All users",
                    mode="markers+lines"
                ))
            else:
                for user in selected_users:
                    algo_user_filtered_df = filtered_df[(filtered_df["Algorithm"] == algorithm) & (filtered_df["User"] == user)]
                    fig.add_trace(go.Scatter(
                        x=algo_user_filtered_df["Fold"],
                        y=algo_user_filtered_df[metric],
                        name=f"{algorithm} - {metric} - User {user}",
                        mode="markers+lines"
                    ))
    fig.update_layout(
        xaxis=dict(title="Fold", dtick=1, tickmode='linear'),
        yaxis_title="Performance",
        legend=dict(title="Measures of performance"),
        yaxis_range=[0, df[metrics].max().max()+increment_yaxis]
    )
    st.plotly_chart(fig, use_container_width=True)