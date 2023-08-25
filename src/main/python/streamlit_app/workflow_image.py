import streamlit as st
import os
from streamlit_app import config
from streamlit_app.workflow.graph_generate import Workflow


# WORKFLOW:
wf = Workflow(config.WORKFLOWS_DESCRIPTION)

def show_wf(wf_name, init_step, with_context=None, optional_value_list=None):
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
