# App Streamlit settings:
APP_TITLE = 'AUTO-DataGenCARS'
APP_ICON = 'resources/icons/logo-datagencars.jpg'
APP_LAYOUT = ['centered', 'centered', 'wide']
APP_INITIAL_SIDEBAR_STATE = ['auto', 'expanded', 'auto', 'collapsed']
APP_DESCRIPTION = 'It is a complete Python-based synthetic dataset generator for the evaluation of Context-Aware Recommendation Systems (CARS) to obtain the required datasets for any type of scenario desired.'

# AUTO-DataGenCARS general options:
GENERAL_OPTIONS = ['Select one option', 'Generate a synthetic dataset', 'Pre-process a dataset', 'Analysis a dataset']

# Generate a synthetic dataset:
RATING_FEEDBACK_OPTIONS = ['Explicit ratings', 'Implicit ratings']
# user:
USER_TYPE = 'user'
USER_PROFILE_TYPE = 'user profile'
USER_PROFILE_SCHEMA_NAME = 'user_profile'
USER_SCHEMA_NAME = 'user_schema'
# item:
ITEM_TYPE = 'item'
ITEM_PROFILE_TYPE = 'item profile'
ITEM_PROFILE_SCHEMA_NAME = 'item_profile'
ITEM_SCHEMA_NAME = 'item_schema'
# context:
CONTEXT_TYPE = 'context'
CONTEXT_SCHEMA_NAME = 'context_schema'
# generation config:
GENERATION_CONFIG_SCHEMA_NAME = 'generation_config'
# rating:
RATING_TYPE = 'rating'

# Pre-process a dataset:
WF_OPTIONS = ['Replace NULL values', 'Generate user profile', 'Replicate dataset', 'Extend dataset', 'Recalculate ratings', 'Cast ratings', 'Data converter']
# WF --> Replace NULL values:
IC_WF_REPLACE_NULL_VALUES=['item', 'context']
I_WF_REPLACE_NULL_VALUES=['item']
GENERATOR_OPTIONS = ['Categorical', 'Numerical', 'Fixed', 'URL', 'Address', 'Date', 'BooleanList', 'Device', 'Position']
ATTRITBUTE_OPTIONS = ['Integer', 'Float', 'String', 'Boolean', 'List', 'AttributeComposite']

# WF --> Generate User Profile:
DATASET_CARS = ['user', 'item', 'context', 'rating']
DATASET_RS = ['user', 'item', 'rating']
UP_OPTIONS = ['Automatic', 'Manual']

# WF --> Converter data:
CONVERTER_DATA_OPTIONS = ['From numerical to categorical', 'From categorical to numerical']

# Analysis a dataset:
ANLYSIS_OPTIONS = ['Visualization', 'Evaluation']

# -------------------------------------------------------------------------------
# Images or icons:
USER_PROFILE = 'resources/icons/user_profile.png'

# JSON files:
WORKFLOWS_DESCRIPTION = 'resources/workflows.json'

# Graphs:
PLOTS_FONT = {'family': 'serif', 'color':  'black', 'weight': 'normal', 'size': 12}
PLOTS_GRID = {'visible':True, 'color':'gray', 'linestyle':'-.', 'linewidth':0.5}

# Metrics:
SCIKIT_LEARN_METRICS = ['Precision', 'Recall', 'F1 score', 'ROC-AUC', 'MAE', 'MSE', 'RMSE']
