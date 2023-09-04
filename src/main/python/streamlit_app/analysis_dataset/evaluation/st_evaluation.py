from streamlit_app.analysis_dataset.evaluation import st_evaluation_cars, st_evaluation_rs


def generate(with_context):
    """
    Generates the evaluation of traditional RS or CARS.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    """    
    # CARS Evaluation:
    if with_context:
        st_evaluation_cars.evaluate()
    # RS Evaluation:
    else:
        st_evaluation_rs.evaluate()
