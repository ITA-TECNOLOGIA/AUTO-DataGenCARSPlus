import streamlit as st
import os
from streamlit_app import config
from workflow.graph_generate import Workflow


# WORKFLOW:
wf = Workflow(config.WORKFLOWS_DESCRIPTION)

def show_wf(with_context, init_step, null_values, wf_name):
    with st.expander(label='Workflow'):
        json_opt_params = {
            'CARS': str(with_context),
            'NULLValues': str(null_values),
            'init_step': init_step,
        }
        path = wf.create_workflow(wf_name, json_opt_params)
        image = st.image(image=path, use_column_width=False, output_format="auto", width=650)
        os.remove(path)       
