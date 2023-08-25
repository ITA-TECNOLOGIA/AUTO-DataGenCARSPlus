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
USER_TYPE = 'user'
ITEM_TYPE = 'item'
CONTEXT_TYPE = 'context'
ITEM_PROFILE_TYPE = 'item profile'
USER_PROFILE_TYPE = 'user profile'
GENERATION_CONFIG_SCHEMA_NAME = 'generation_config'
USER_SCHEMA_NAME = 'user_schema'
ITEM_SCHEMA_NAME = 'item_schema'
CONTEXT_SCHEMA_NAME = 'context_schema'
ITEM_PROFILE_SCHEMA_NAME = 'item_profile'
USER_PROFILE_SCHEMA_NAME = 'user_profile'


# Pre-process a dataset:
WF_OPTIONS = ['Replicate dataset', 'Extend dataset', 'Recalculate ratings', 'Replace NULL values', 'Generate user profile', 'Ratings to binary', 'Mapping categorization']

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

# App Constants
ATR_OPTS = ['Integer', 'Float', 'String', 'Boolean', 'List', 'AttributeComposite']
GENERATOR_OPTS = ['Integer/Float/String/Boolean (following a distribution)', 'Fixed', 'URL', 'Address', 'Date', 'BooleanList']
