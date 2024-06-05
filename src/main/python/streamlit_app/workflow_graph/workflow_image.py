import os

import streamlit as st
from streamlit_app import config
from streamlit_app.workflow_graph.graph_generate import Workflow

# WORKFLOW:
wf = Workflow(config.WORKFLOWS_DESCRIPTION)

def show_wf(wf_name, init_step, with_context=None, optional_value_list=None):
    """
    Display a workflow with an expander and image.
    :param wf_name: The name of the workflow to display.
    :param init_step: The initial step of the workflow.
    :param with_context: It is True if the dataset to be generated will have contextual information, and False otherwise.
    :param optional_value_list: Optional key-value pairs to include in the workflow parameters.    
    """
    with st.expander(label='Workflow'):
        json_opt_params = {
            'CARS': str(with_context),            
            'init_step': init_step            
        }
        if optional_value_list:
            for optional_value in optional_value_list:
                json_opt_params[optional_value[0]] = optional_value[1]
        path = wf.create_workflow(wf_name, json_opt_params)
        image = st.image(image=path, use_column_width=False, output_format="auto", width=650)
        os.remove(path)   
