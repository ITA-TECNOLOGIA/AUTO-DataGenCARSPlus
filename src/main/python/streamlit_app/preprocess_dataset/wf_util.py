# import altair as alt
# import numpy as np
# from datetime import date
# import plotly.graph_objs as go
# import datagencars.evaluation.rs_surprise.evaluation as evaluation
import base64

import pandas as pd
import streamlit as st


####### Common methods ######
def save_file(file_name, file_value, extension):
    """
    Save a schema file.
    :param file_name: The name of the schema file.
    :param file_value: The content of the schema file.
    :param extension: The file extension ('*.conf' or '*.csv').
    """
    if extension == 'conf':
        link_file = f'<a href="data:text/plain;base64,{base64.b64encode(file_value.encode()).decode()}" download="{file_name}.{extension}">Download</a>'
    elif extension == 'csv':
        link_file = f'<a href="data:file/csv;base64,{base64.b64encode(file_value.encode()).decode()}" download="{file_name}.{extension}">Download</a>'
    st.markdown(link_file, unsafe_allow_html=True)    

def save_df(df_name, df_value, extension):
    """
    Save a df file.
    :param df_name: The df file name.
    :param df_value: The df file content.
    :param extension: The file extension ('*.csv').
    """
    link_df = f'<a href="data:file/csv;base64,{base64.b64encode(df_value.to_csv(index=False).encode()).decode()}" download="{df_name}.{extension}">Download</a>'
    st.markdown(link_df, unsafe_allow_html=True)

def show_schema_file(schema_file_name, schema_value):
    """
    Show the content of the specified schema file.
    :param schema_file_name: The schema file name.
    :param schema_value: The schema file content.
    """
    with st.expander(f"Show {schema_file_name}.conf"):
        st.text_area(label='Current file:', value=schema_value, height=500, disabled=True, key=f'true_edit_{schema_file_name}')

def load_dataset(file_type_list, wf_type):
    """
    Loads dataset files (user.csv, item.csv, context.csv and rating.csv) in dataframes.
    :param file_type_list: List of file types.
    :return: Dataframes related to the uploaded dataset files.
    """
    user_df = pd.DataFrame()
    item_df = pd.DataFrame()
    context_df = pd.DataFrame()
    rating_df = pd.DataFrame()
    user_profile_df = pd.DataFrame()
    # Uploading a dataset:
    if 'user' in file_type_list:
        user_df = load_one_file(file_type='user', wf_type=wf_type)
    if 'item' in file_type_list:
        item_df = load_one_file(file_type='item', wf_type=wf_type)
    if 'context' in file_type_list:
        context_df = load_one_file(file_type='context', wf_type=wf_type)   
    if 'rating' in file_type_list:
        rating_df = load_one_file(file_type='rating', wf_type=wf_type)
    if 'user profile' in file_type_list:
        user_profile_df = load_one_file(file_type='user_profile', wf_type=wf_type)
    return user_df, item_df, context_df, rating_df, user_profile_df

def load_one_file(file_type, wf_type):
    """
    Load only one file (user.csv, item.csv, context.csv or rating.csv).
    :param file_type: The file type.
    :return: A dataframe with the information of uploaded file.
    """
    df = pd.DataFrame()    
    with st.expander(f"Upload your {file_type}.csv file"):
        separator = st.text_input(label=f"Enter the separator for your {file_type}.csv file (default is ';')", value=";", key=f'text_input_{file_type}_{wf_type}')
        uploaded_file = st.file_uploader(label=f"Select {file_type}.csv file", type="csv", key=f'uploaded_file_{file_type}_{wf_type}')
        if uploaded_file is not None:
            if not separator:
                st.error('Please provide a separator.')
            else:
                # Read the header of the file to determine column names
                header = uploaded_file.readline().decode("utf-8").strip()
                column_names = header.split(separator)
                # Rename columns
                for i, col in enumerate(column_names):
                    if "user" in col.lower() and "id" in col.lower() and "profile" not in col.lower():
                        column_names[i] = "user_id"
                    elif "item" in col.lower() and "id" in col.lower():
                        column_names[i] = "item_id"
                    elif "context" in col.lower() and "id" in col.lower():
                        column_names[i] = "context_id"
                try:                    
                    df = pd.read_csv(uploaded_file, sep=separator, names=column_names)                             
                    st.dataframe(df.head())
                except Exception as e:
                    st.error(f"An error occurred while reading the {file_type} file: {str(e)}")
                    df = None
    return df


# ####### Analysis a dataset #######
# # VISUALIZATION:
# def plot_column_attributes_count(data, column, sort):
#     """
#     Plot the number of values by attribute.
#     :param data: TODO
#     :param column: TODO
#     :param sort: TODO
#     """
#     if sort == 'asc':
#         sort_field = alt.EncodingSortField('count', order='ascending')
#     elif sort == 'desc':
#         sort_field = alt.EncodingSortField('count', order='descending') 
#     else:
#         sort_field = None
#     chart = alt.Chart(data).mark_bar().encode(
#         x=alt.X(column + ':O', title='Attribute values', sort=sort_field),
#         y=alt.Y('count:Q', title='Count'),
#         tooltip=[column, 'count']
#     ).interactive()
#     st.altair_chart(chart, use_container_width=True)
            
# def print_statistics_by_attribute(statistics):
#     """
#     Prints in streamlit statistics by attribute.
#     :param statistics: The statistics.    
#     """
#     for stat in statistics:
#         st.subheader(stat[0])
#         st.write('Average: ', stat[1])
#         st.write('Standard deviation: ', stat[2])
#         col1, col2 = st.columns(2)
#         with col1:
#             st.write('Frequencies:')
#             st.dataframe(stat[3])
#         with col2:
#             st.write('Percentages:')
#             st.dataframe(stat[4])

# def correlation_matrix(df, label):
#     """
#     Determines the correlation matrix.
#     :param label: TODO
#     :param df: TODO
#     :return: A correlation matrix.
#     """
#     corr_matrix = pd.DataFrame()
#     columns_id = df.filter(regex='_id$').columns.tolist()
#     columns_not_id = [col for col in df.columns if col not in columns_id]
#     data_types = []
#     for col in columns_not_id:     
#         data_types.append({"Attribute": col, "Data Type": str(df[col].dtype)})
#         break    
#     selected_columns = st.multiselect("Select columns to analyze", columns_not_id, key='cm_'+label)
#     method = st.selectbox("Select a method", ['pearson', 'kendall', 'spearman'], key='method_'+label)
#     if st.button("Generate correlation matrix", key='button_'+label) and selected_columns:
#         with st.spinner("Generating correlation matrix..."):
#             merged_df_selected = df[selected_columns].copy()
#             # Categorize non-numeric columns using label encoding:
#             for col in merged_df_selected.select_dtypes(exclude=[np.number]):
#                 merged_df_selected[col], _ = merged_df_selected[col].factorize()            
#             corr_matrix = merged_df_selected.corr(method=method)     
#     return corr_matrix       

# # EVALUATION:
# def select_params(algorithm):
#     """
#     Select parameters of the specified recommendation algorithm.
#     :param algorithm: A recommendation algorithm.
#     :return: A dictionary with parameter values.
#     """
#     if algorithm == "SVD":
#         st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
#         return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_svd'),
#                 "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_svd'),
#                 "lr_all": st.sidebar.number_input("Learning rate for all parameters", min_value=0.0001, max_value=1.00, value=0.005, step=0.0001, key='lr_all_svd'),
#                 "reg_all": st.sidebar.number_input("Regularization term for all parameters", min_value=0.0001, max_value=1.00, value=0.02, key='reg_all_svd')}
#     if algorithm == "BaselineOnly":
#         st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
#         return {"bsl_options": {"method": st.sidebar.selectbox("Baseline method", ["als", "sgd"], key='method_baselineonly'),
#                                 "reg_i": st.sidebar.number_input("Regularization term for item parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_i_baselineonly'),
#                                 "reg_u": st.sidebar.number_input("Regularization term for user parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_u_baselineonly')}}
#     if algorithm == "CoClustering":
#         st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
#         return {"n_cltr_u": st.sidebar.number_input("Number of clusters for users", min_value=1, max_value=1000, value=5),
#                 "n_cltr_i": st.sidebar.number_input("Number of clusters for items", min_value=1, max_value=1000, value=5)}
#     if algorithm == "NMF":
#         st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
#         return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_nmf'),
#                 "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_nmf'),
#                 "reg_pu": st.sidebar.number_input("Regularization term for user factors", min_value=0.0001, max_value=1.0, value=0.02),
#                 "reg_qi": st.sidebar.number_input("Regularization term for item factors", min_value=0.0001, max_value=1.0, value=0.02)}
#     if algorithm == "NormalPredictor":
#         return {}
#     if algorithm == "SlopeOne":
#         return {}
#     if algorithm == "SVDpp":
#         st.sidebar.markdown(f'**{algorithm} parameter settings:**')          
#         return {"n_factors": st.sidebar.number_input("Number of factors", min_value=1, max_value=1000, value=100, key='n_factors_svdpp'),
#                 "n_epochs": st.sidebar.number_input("Number of epochs", min_value=1, max_value=1000, value=20, key='n_epochs_svdpp'),
#                 "lr_all": st.sidebar.number_input("Learning rate for all parameters", min_value=0.0001, max_value=1.0, value=0.005, key='lr_all_svdpp'),
#                 "reg_all": st.sidebar.number_input("Regularization term for all parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_all_svdpp')}
#     if algorithm == "KNNBasic":
#         return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbasic'),
#                 "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["pearson", "msd", "cosine"], key='sim_options_knnbasic'),
#                                 "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnbasic')}}
#     if algorithm == "KNNWithMeans":
#         return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnwithmeans'),
#                 "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["pearson", "msd", "cosine"], key='sim_options_knnwithmeans'),
#                                 "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnwithmeans')}}
#     if algorithm == "KNNWithZScore":
#         return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnwithzscore'),
#                 "min_k": st.sidebar.number_input("Minimum number of nearest neighbors", min_value=1, max_value=1000, value=1, key='min_k_knnwithzscore'),
#                 "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["pearson", "msd", "cosine"], key='sim_options_knnwithzscore'),
#                                 "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnwithzscore')}}
#     if algorithm == "KNNBaseline":
#         return {"k": st.sidebar.number_input("Number of nearest neighbors", min_value=1, max_value=1000, value=40, key='k_knnbaseline'),
#                 "sim_options": {"name": st.sidebar.selectbox("Similarity measure", ["pearson", "msd", "cosine"], key='sim_options_knnbaseline'),
#                                 "user_based": st.sidebar.selectbox("User-based or item-based", ["user", "item"], key='user_based_knnbaseline')},
#                 "bsl_options": {"method": st.sidebar.selectbox("Baseline method", ["als", "sgd"], key='method_knnbaseline'),
#                                 "reg_i": st.sidebar.number_input("Regularization term for item parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_i_knnbaseline'),
#                                 "reg_u": st.sidebar.number_input("Regularization term for user parameters", min_value=0.0001, max_value=1.0, value=0.02, key='reg_u_knnbaseline')}}

# def select_params_contextual(algorithm):
#     """
#     Select parameters of the specified context-aware recommendation algorithm.
#     :param algorithm: A context-aware recommendation algorithm.
#     :return: A dictionary with parameter values.
#     """
#     if algorithm == "KNeighborsClassifier":
#         return {"n_neighbors": st.sidebar.number_input("Number of neighbors", min_value=1, max_value=1000, value=5, key='n_neighbors_kneighborsclassifier'),
#                 "weights": st.sidebar.selectbox("Weights", ["uniform", "distance"], key='weights_kneighborsclassifier'),
#                 "algorithm": st.sidebar.selectbox("Algorithm", ["auto", "ball_tree", "kd_tree", "brute"], key='algorithm_kneighborsclassifier'),
#                 "leaf_size": st.sidebar.number_input("Leaf size", min_value=1, max_value=1000, value=30, key='leaf_size_kneighborsclassifier'),
#                 "p": st.sidebar.number_input("P", min_value=1, max_value=1000, value=2, key='p_kneighborsclassifier'),
#                 "metric": st.sidebar.selectbox("Metric", ["minkowski", "euclidean", "manhattan", "chebyshev", "seuclidean", "mahalanobis", "wminkowski", "haversine"], key='metric_kneighborsclassifier'),
#                 "n_jobs": st.sidebar.number_input("Number of jobs", min_value=1, max_value=1000, value=1, key='n_jobs_kneighborsclassifier')}
#     elif algorithm == "SVC":
#         return {"C": st.sidebar.number_input("C", min_value=0.0001, max_value=1000.0, value=1.0, key='C_svc'),
#                 "kernel": st.sidebar.selectbox("Kernel", ["linear", "poly", "rbf", "sigmoid", "precomputed"], key='kernel_svc'),
#                 "degree": st.sidebar.number_input("Degree", min_value=1, max_value=1000, value=3, key='degree_svc'),
#                 "gamma": st.sidebar.selectbox("Gamma", ["scale", "auto"], key='gamma_svc'),
#                 "coef0": st.sidebar.number_input("Coef0", min_value=0.0, max_value=1000.0, value=0.0, key='coef0_svc'),
#                 "shrinking": st.sidebar.checkbox("Shrinking?", key='shrinking_svc'),
#                 "probability": st.sidebar.checkbox("Probability?", key='probability_svc'),
#                 "tol": st.sidebar.number_input("Tol", min_value=0.0001, max_value=1000.0, value=0.001, key='tol_svc'),
#                 "cache_size": st.sidebar.number_input("Cache size", min_value=0.0001, max_value=1000.0000, value=200.0000, key='cache_size_svc'),
#                 "class_weight": st.sidebar.selectbox("Class weight", ["balanced", None], key='class_weight_svc'),
#                 "verbose": st.sidebar.checkbox("Verbose?", key='verbose_svc'),
#                 "max_iter": st.sidebar.number_input("Maximum iterations", min_value=-1, max_value=1000, value=-1, key='max_iter_svc'),
#                 "decision_function_shape": st.sidebar.selectbox("Decision function shape", ["ovo", "ovr"], key='decision_function_shape_svc'),
#                 "random_state": st.sidebar.number_input("Random state", min_value=-0.5, max_value=1000.0, value=-0.5, key='random_state_svc'),
#                 "break_ties": st.sidebar.checkbox("Break ties?", key='break_ties_svc')}
#     elif algorithm == "GaussianNB":
#         return {}
#     elif algorithm == "RandomForestClassifier":
#         return {"n_estimators": st.sidebar.number_input("Number of estimators", min_value=1, max_value=1000, value=100, key='n_estimators_randomforestclassifier'),
#                 "criterion": st.sidebar.selectbox("Criterion", ["gini", "entropy"], key='criterion_randomforestclassifier'),
#                 "max_depth": st.sidebar.number_input("Maximum depth", min_value=-0.5, max_value=1000.0, value=-0.5, key='max_depth_randomforestclassifier'),
#                 "min_samples_split": st.sidebar.number_input("Minimum samples split", min_value=1, max_value=1000, value=2, key='min_samples_split_randomforestclassifier'),
#                 "min_samples_leaf": st.sidebar.number_input("Minimum samples leaf", min_value=1, max_value=1000, value=1, key='min_samples_leaf_randomforestclassifier'),
#                 "min_weight_fraction_leaf": st.sidebar.number_input("Minimum weight fraction leaf", min_value=0.0001, max_value=1.0, value=0.01, key='min_weight_fraction_leaf_randomforestclassifier'),
#                 "max_features": st.sidebar.selectbox("Maximum features", ["auto", "sqrt", "log2", None], key='max_features_randomforestclassifier'),
#                 "max_leaf_nodes": st.sidebar.number_input("Maximum leaf nodes", min_value=-0.5, max_value=1000.0, value=-0.5, key='max_leaf_nodes_randomforestclassifier'),
#                 "min_impurity_decrease": st.sidebar.number_input("Minimum impurity decrease", min_value=0.0001, max_value=1.0, value=0.01, key='min_impurity_decrease_randomforestclassifier'),
#                 "bootstrap": st.sidebar.checkbox("Bootstrap?", key='bootstrap_randomforestclassifier'),
#                 "oob_score": st.sidebar.checkbox("OOB score?", key='oob_score_randomforestclassifier'),
#                 "n_jobs": st.sidebar.number_input("Number of jobs", min_value=-0.5, max_value=1000.0, value=-0.5, key='n_jobs_randomforestclassifier'),
#                 "random_state": st.sidebar.number_input("Random state", min_value=-0.5, max_value=1000.0, value=-0.5, key='random_state_randomforestclassifier'),
#                 "verbose": st.sidebar.number_input("Verbose", min_value=0, max_value=1000, value=0, key='verbose_randomforestclassifier'),
#                 "ccp_alpha": st.sidebar.number_input("CCP alpha", min_value=0.0001, max_value=1.0, value=0.01, key='ccp_alpha_randomforestclassifier'),
#                 "class_weight": st.sidebar.selectbox("Class weight", ["balanced", "balanced_subsample", None], key='class_weight_randomforestclassifier'),
#                 "max_samples": st.sidebar.number_input("Maximum samples", min_value=-0.5, max_value=1.0, value=-0.5, key='max_samples_randomforestclassifier'),
#                 "warm_start": st.sidebar.checkbox("Warm start?", key='warm_start_randomforestclassifier')}
#     elif algorithm == "KMeans":
#         return {"n_clusters": st.sidebar.number_input("Number of clusters", min_value=1, max_value=1000, value=5, key='n_clusters_kmeans'),
#                 "init": st.sidebar.selectbox("Initialization method", ["k-means++", "random"], key='init_kmeans'),
#                 "n_init": st.sidebar.number_input("Number of initializations", min_value=1, max_value=1000, value=10, key='n_init_kmeans'),
#                 "max_iter": st.sidebar.number_input("Maximum number of iterations", min_value=1, max_value=1000, value=300, key='max_iter_kmeans'),
#                 "tol": st.sidebar.number_input("Tolerance", min_value=0.0001, max_value=1.0, value=0.0001, key='tol_kmeans')}
#     elif algorithm == "HistGradientBoostingClassifier":
#         return {"learning_rate": st.sidebar.slider("Learning rate", 0.01, 1.0, 0.1, step=0.01),
#                 "max_iter": st.sidebar.slider("Max number of iterations", 10, 1000, 100, step=10),
#                 "max_leaf_nodes": st.sidebar.slider("Max leaf nodes", 10, 200, 31, step=1),
#                 "max_depth": st.sidebar.slider("Max depth", 1, 50, 15, step=1),
#                 "l2_regularization": st.sidebar.slider("L2 regularization", 0.0, 1.0, 0.0, step=0.01)}
    
# def select_split_strategy(strategy):
#     """
#     Select parameters related to the specified split strategy (RS).
#     :param strategy: The split strategy.
#     :return: A dictionary with parameter values. 
#     """
#     if strategy == "KFold":
#         st.sidebar.markdown("""A basic cross-validation iterator. Each fold is used once as a testset while the k - 1 remaining folds are used for training.""")
#         return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
#                 "shuffle": st.sidebar.checkbox("Shuffle?")}
#     elif strategy == "RepeatedKFold":
#         st.sidebar.markdown("""Repeats KFold n times with different randomization in each repetition.""")
#         return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
#                 "n_repeats": st.sidebar.number_input("Number of repeats", min_value=1, max_value=10, value=1)}
#     elif strategy == "ShuffleSplit":
#         st.sidebar.markdown("""A basic cross-validation iterator with random trainsets and testsets. Contrary to other cross-validation strategies, random splits do not guarantee that all folds will be different, although this is still very likely for sizeable datasets.""")
#         return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
#                 "test_size": st.sidebar.number_input("Test size", min_value=0.1, max_value=0.9, step=0.1, value=0.2),
#                 "shuffle": st.sidebar.checkbox("Shuffle?")}
#     elif strategy == "LeaveOneOut":
#         st.sidebar.markdown("""Cross-validation iterator where each user has exactly one rating in the testset. Contrary to other cross-validation strategies, LeaveOneOut does not guarantee that all folds will be different, although this is still very likely for sizeable datasets.""")
#         return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
#                 "min_n_ratings": st.sidebar.number_input("Minimum number of ratings for each user (trainset)", min_value=0, max_value=10000, value=0)}
    
# def select_split_strategy_contextual(strategy):
#     """
#     Select parameters related to the specified split strategy (CARS).
#     :param strategy: The split strategy.
#     :return: A dictionary with parameter values. 
#     """
#     if strategy == "ShuffleSplit":
#         n_splits = st.sidebar.number_input("Number of splits", 2, 100, 10)
#         train_size = st.sidebar.slider("Train set size (0.0 to 1.0)", 0.01, 1.0, 0.2, step=0.01)        
#         return {"n_splits": n_splits, "train_size": train_size}
#     elif strategy == "KFold":
#         n_splits = st.sidebar.number_input("Number of folds", 2, 100, 5)             
#         return {"n_splits": n_splits, "shuffle": st.sidebar.checkbox("Shuffle?")}
#     elif strategy == "LeaveOneOut":
#         st.sidebar.markdown("""Cross-validation iterator where each user has exactly one rating in the testset. Contrary to other cross-validation strategies, LeaveOneOut does not guarantee that all folds will be different, although this is still very likely for sizeable datasets.""")
#         return {"n_splits": st.sidebar.number_input("Number of folds", min_value=2, max_value=10, value=5),
#                 "min_n_ratings": st.sidebar.number_input("Minimum number of ratings for each user (trainset)", min_value=0, max_value=10000, value=0)}

# def evaluate_algo(algo_list, strategy_instance, metrics, data):
#     """
#     Evaluates recommendation algorithms.
#     :param algo_list: Recommendation algorithms.
#     :param strategy_instance: Split strategy.
#     :param metrics: The evaluation metrics.
#     :param data: Recommendation data.
#     :return: A dataframe with evaluation results.
#     """
#     results = []
#     fold_counter = {} # To count the number of folds for each algorithm
#     fold_count = 0
#     with st.spinner("Evaluating algorithms..."):
#         for algo in algo_list:
#             fold_count += 1
#             cross_validate_results = evaluation.cross_validate(algo, data, measures=metrics, cv=strategy_instance)
#             for i in range(strategy_instance.n_splits):
#                 row = {}
#                 algo_name = type(algo).__name__
#                 row["Algorithm"] = algo_name

#                 # Modify the name of the metrics to be more readable
#                 for key, value in cross_validate_results.items():
#                     if key == "fit_time":
#                         row["Time (train)"] = value[i]
#                     elif key == "test_time":
#                         row["Time (test)"] = value[i]
#                     elif key == "test_f1_score":
#                         row["F1_Score"] = value[i]
#                     elif key == "test_recall":
#                         row["Recall"] = value[i]
#                     elif key == "test_precision":
#                         row["Precision"] = value[i]
#                     elif key == "test_auc_roc":
#                         row["AUC-ROC"] = value[i]
#                     else:
#                         row[key.replace("test_", "").upper()] = value[i]
                    
#                 if algo_name in fold_counter:
#                     fold_counter[algo_name] += 1
#                 else:
#                     fold_counter[algo_name] = 1
#                 row["Fold"] = fold_counter[algo_name]

#                 results.append(row)
#     df = pd.DataFrame(results)
#     cols = ["Fold"] + [col for col in df.columns if col != "Fold"] # Move the "Fold" column to the first position
#     df = df[cols]
#     return df

# def visualize_graph_mean_rs(df, increment_yaxis):
#     """
#     Visualize mean results of the evaluation of recommendation algorithms.   
#     :param df: A dataframe with evaluation mean results.
#     :param increment_yaxis: A float value to increase the maximum value of the Y-axis.    
#     """
#     # Create trace for each column:
#     fig = go.Figure()
#     for column in df.columns[1:]:
#         fig.add_trace(go.Bar(x=df['Algorithm'], y=df[column], name=column))      
#     # Create figure:
#     selected_metric_list = df.columns[1:].tolist()
#     fig.update_layout(title='Performance Comparison of Recommendation Algorithms',
#                       xaxis_title='Recommendation Algorithm',
#                       yaxis_title='Performance',
#                       legend=dict(title="Metrics"),
#                       barmode='group',
#                       yaxis_range=[0, df[selected_metric_list].max().max()+increment_yaxis])
#     # Show plot:                        
#     st.plotly_chart(fig, use_container_width=True)

# def visualize_graph_fold_rs(df, metric, increment_yaxis):
#     """
#     Visualize fold results by metric of the evaluation of recommendation algorithms.   
#     :param df: A dataframe with evaluation results by fold.
#     :param metric: The metric measure.
#     :param increment_yaxis: A float value to increase the maximum value of the Y-axis.    
#     """
#     algorithms = df["Algorithm"].unique()
#     fig = go.Figure()
#     for algorithm in algorithms:
#         # Filter the dataframe for the current algorithm
#         filtered_df = df[df["Algorithm"] == algorithm]

#         # Create the line chart for the current metric
#         fig.add_trace(go.Scatter(
#             x=filtered_df["Fold"],
#             y=filtered_df[metric],
#             name=algorithm
#         ))
#     fig.update_layout(
#         xaxis_title="Fold",
#         yaxis_title="Performance",
#         legend=dict(title="Recommendation algorithms"),
#         yaxis_range=[0, df[metric].max().max()+increment_yaxis]
#     )
#     st.plotly_chart(fig, use_container_width=True)

# def visualize_graph_fold_cars(df, algorithms, metrics, selected_users, increment_yaxis):
#     """
#     Visualize a line graphic with evaluation results considering different algorithms, metrics and users.
#     :param df: A dataframe with evaluation results.
#     :param algorithms: List of recommendation algorithms.
#     :param metrics: List of metrics.
#     :param selected_users: List of users.
#     """
#     filtered_df = df[df["Algorithm"].isin(algorithms)]
#     fig = go.Figure()
#     for algorithm in algorithms:
#         for metric in metrics:
#             if "All users" in selected_users:
#                 users = df["User"].unique()
#                 algo_filtered_df = filtered_df[(filtered_df["Algorithm"] == algorithm) & (filtered_df["User"].isin(users))]
#                 mean_values = []
#                 for fold in algo_filtered_df["Fold"].unique():
#                     fold_filtered_df = algo_filtered_df[algo_filtered_df["Fold"] == fold]
#                     mean_value = fold_filtered_df[metric].mean()
#                     mean_values.append(mean_value)
#                 fig.add_trace(go.Scatter(
#                     x=algo_filtered_df["Fold"].unique(),
#                     y=mean_values,
#                     name=f"{algorithm} - {metric} - All users",
#                     mode="markers+lines"
#                 ))
#             else:
#                 for user in selected_users:
#                     algo_user_filtered_df = filtered_df[(filtered_df["Algorithm"] == algorithm) & (filtered_df["User"] == user)]
#                     fig.add_trace(go.Scatter(
#                         x=algo_user_filtered_df["Fold"],
#                         y=algo_user_filtered_df[metric],
#                         name=f"{algorithm} - {metric} - User {user}",
#                         mode="markers+lines"
#                     ))
#     fig.update_layout(
#         xaxis=dict(title="Fold", dtick=1, tickmode='linear'),
#         yaxis_title="Performance",
#         legend=dict(title="Measures of performance"),
#         yaxis_range=[0, df[metrics].max().max()+increment_yaxis]
#     )
#     st.plotly_chart(fig, use_container_width=True)

# def visualize_graph_mean_cars(df, algorithms, metrics, selected_users, increment_yaxis):
#     """
#     Visualize a bar graphic with evaluation results considering different algorithms, metrics and users.
#     :param df: A dataframe with evaluation results.
#     :param algorithms: List of recommendation algorithms.
#     :param metrics: List of metrics.
#     :param selected_users: List of users.
#     """
#     fig = go.Figure()
#     for algorithm in algorithms:
#         filtered_df = df[df["Algorithm"] == algorithm]
#         for metric in metrics:
#             if "All users" in selected_users:
#                 users = df["User"].unique()
#                 user_label = "All users"
#                 user_filtered_df = filtered_df[filtered_df["User"].isin(users)]
#                 mean_value = user_filtered_df[metric].mean()
#                 fig.add_trace(go.Bar(
#                     x=[f"{metric}"],
#                     y=[mean_value],
#                     name=f"{algorithm} - {user_label}",
#                     legendgroup=f"{algorithm} - {user_label}"
#                 ))
#             else:
#                 for user in selected_users:
#                     user_filtered_df = filtered_df[filtered_df["User"] == user]
#                     mean_value = user_filtered_df[metric].mean()
#                     fig.add_trace(go.Bar(
#                         x=[f"{metric}"],
#                         y=[mean_value],
#                         name=f"{algorithm} - User {user}",
#                         legendgroup=f"{algorithm} - User {user}"
#                     ))
#     fig.update_layout(
#         xaxis_title="Measures of performance",
#         yaxis_title="Performance",
#         legend=dict(title="Algorithms & Users"),
#         barmode='group',
#         yaxis_range=[0, df[metrics].max().max()+increment_yaxis]
#     )
#     st.plotly_chart(fig, use_container_width=True)

# def select_contextual_features(df, label):
#     """
#     Gets a sub-dataframe with the user-selected item or context features (from item_df or context_df, respectively).
#     :param df: The item or context dataframe.
#     :param label: The item or context label ("item" or "context").
#     ;return: A sub-dataframe with the user-selected item or context features.
#     """
#     column_names = df.columns[1:].tolist() # Excluding the item_id or context_id.    
#     selected_columns = st.sidebar.multiselect(label=f'Select {label} features:', options=column_names, default=column_names)
#     if selected_columns:
#         return df[[label+'_id']+selected_columns]
    
# def replace_with_none(params):
#     """
#     TODO
#     :param params: TODO
#     :return: TODO
#     """
#     for key, value in params.items():
#         if value == -0.5:
#             params[key] = None
#     return params

