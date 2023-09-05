import console
import plotly.graph_objs as go
import streamlit as st
from streamlit_app import config, help_information
from streamlit_app.analysis_dataset.evaluation import (st_evaluation_cars_cm,
                                                       st_evaluation_cars_post,
                                                       st_evaluation_cars_pre)
from streamlit_app.preprocess_dataset import wf_util


def evaluate():
    """
    Evaluating Context-Aware Recommendation Systems.
    """
    output = st.empty() 
    with console.st_log(output.code): 
        # Loading rating file:
        st.write('Upload the following file: ')
        rating_df = wf_util.load_one_file(file_type=config.RATING_TYPE, wf_type='evaluation_cars_rating_df')         
        st.sidebar.markdown("""---""")
        
        if not rating_df.empty:
            print('The rating file has been uploaded.')   
            
            # SELECTING PARADIGM TO EVALUATE:
            st.sidebar.markdown('**CARS paradigm selection**')
            paradigm = st.sidebar.selectbox(label="Select one paradigm:", options=config.PARDIGM_OTPIONS)
            st.header(f'Evaluation of CARS: {paradigm}')                

            # CONTEXTUAL MODELING:
            if paradigm == "Contextual Modeling":                
                help_information.help_contextual_modeling_paradigm()
                st_evaluation_cars_cm.evaluate_cm_paradigm(rating_df)                
                print('The contextual modeling paradigm has been evaluated.')
            # POST-FILTERING:
            elif paradigm == "Post-filtering":            
                help_information.help_postfiltering_paradigm()
                st_evaluation_cars_post.evaluate_postfiltering_paradigm(rating_df)
                print('The pre-filtering paradigm has been evaluated.')
            # PRE-FILTERING:
            else:
                help_information.help_prefiltering_paradigm()
                st_evaluation_cars_pre.evaluate_prefiltering_paradigm(rating_df)
                print('The post-filtering paradigm has been evaluated.')        
        else:
            st.warning("The rating file has not been uploaded.")    
    
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
                fig.add_trace(go.Bar(x=[f"{metric}"], y=[mean_value], name=f"{algorithm} - {user_label}", legendgroup=f"{algorithm} - {user_label}"))
            else:
                for user in selected_users:
                    user_filtered_df = filtered_df[filtered_df["User"] == user]
                    mean_value = user_filtered_df[metric].mean()
                    fig.add_trace(go.Bar(x=[f"{metric}"], y=[mean_value], name=f"{algorithm} - User {user}", legendgroup=f"{algorithm} - User {user}"))
    fig.update_layout(xaxis_title="Measures of performance", yaxis_title="Performance", legend=dict(title="Algorithms & Users"), barmode='group', yaxis_range=[0, df[metrics].max().max()+increment_yaxis])
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
                fig.add_trace(go.Scatter(x=algo_filtered_df["Fold"].unique(), y=mean_values, name=f"{algorithm} - {metric} - All users", mode="markers+lines"))
            else:
                for user in selected_users:
                    algo_user_filtered_df = filtered_df[(filtered_df["Algorithm"] == algorithm) & (filtered_df["User"] == user)]
                    fig.add_trace(go.Scatter(x=algo_user_filtered_df["Fold"], y=algo_user_filtered_df[metric], name=f"{algorithm} - {metric} - User {user}", mode="markers+lines"))
    fig.update_layout(xaxis=dict(title="Fold", dtick=1, tickmode='linear'), yaxis_title="Performance", legend=dict(title="Measures of performance"), yaxis_range=[0, df[metrics].max().max()+increment_yaxis])
    st.plotly_chart(fig, use_container_width=True)
