#### App Streamlit settings ####:
APP_TITLE = 'AUTO-DataGenCARS'
APP_ICON = 'resources/icons/logo-datagencars.jpg'
APP_LAYOUT = ['centered', 'centered', 'wide']
APP_INITIAL_SIDEBAR_STATE = ['auto', 'expanded', 'auto', 'collapsed']
APP_DESCRIPTION = 'It is a complete Python-based synthetic dataset generator for the evaluation of Context-Aware Recommendation Systems (CARS) to obtain the required datasets for any type of scenario desired.'
#### User information register ####:
USER_INFORMATION_LOG_PATH = 'resources/user_information_log/user_information_log.csv'
IP_LABEL = 'ip'
COUNTRY_LABEL = 'country'
CITY_LABEL = 'city'
REGION_LABEL = 'region'
LOC_LABEL = 'loc'
TIMEZONE_LABEL = 'timezone'
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#### AUTO-DataGenCARS general options ####:
GENERAL_OPTIONS = ['Select one option', 'Generate a synthetic dataset', 'Pre-process a dataset', 'Analysis a dataset', 'Dashboard']
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#### Generate a synthetic dataset ####:
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
# behavior:
BEHAVIOR_TYPE = 'behavior'
EXAMPLE_ROOM_LIST = [{'id': 1, 'x_min': -51.69645309448242, 'x_max': 17.033428192138672, 'y_min': -8.163072506091242e-15, 'y_max': 5.32511043548584, 'z_min': -36.15760040283203, 'z_max': 33.79861068725586}]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#### Pre-process a dataset ####:
WF_OPTIONS = ['Replace NULL values', 'Generate user profile', 'Replicate dataset', 'Extend dataset', 'Recalculate ratings', 'Cast ratings', 'Data converter']
# WF --> Replace NULL values:
IC_WF_REPLACE_NULL_VALUES=['item', 'context']
I_WF_REPLACE_NULL_VALUES=['item']
GENERATOR_OPTIONS = ['Categorical', 'Numerical', 'Fixed', 'URL', 'Address', 'Date', 'BooleanList', 'Device', 'Position']
ATTRITBUTE_OPTIONS = ['Integer', 'Float', 'String', 'Boolean', 'List', 'AttributeComposite']
# WF --> Generate User Profile:
USER_PROFILE_IMAGE = 'resources/icons/user_profile.png'
DATASET_CARS = ['user', 'item', 'context', 'rating']
DATASET_RS = ['user', 'item', 'rating']
UP_OPTIONS = ['Automatic', 'Manual']
# WF --> Converter data:
CONVERTER_DATA_OPTIONS = ['From numerical to categorical', 'From categorical to numerical']
# Workflows:
# JSON files:
WORKFLOWS_DESCRIPTION = 'resources/workflows.json'
# Graphs:
PLOTS_FONT = {'family': 'serif', 'color':  'black', 'weight': 'normal', 'size': 12}
PLOTS_GRID = {'visible':True, 'color':'gray', 'linestyle':'-.', 'linewidth':0.5}
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#### Analysis a dataset ####:
ANLYSIS_OPTIONS = ['Visualization', 'Evaluation']
# Visualization:
VISUALIZATION_OPTIONS = ['Explicit ratings', 'Implicit ratings']

# Evaluation:
# RS:
BASIC_RS=['BaselineOnly', 'NormalPredictor']
CF_RS = ['KNNBasic', 'KNNWithMeans', 'KNNWithZScore', 'KNNBaseline', 'SVD', 'SVDpp', 'NMF', 'SlopeOne', 'CoClustering']
CB_RS = ['PENDING TODO']
# CARS:
PARDIGM_OTPIONS = ["Contextual Modeling", "Pre-filtering", "Post-filtering"]
# CARS --> Contextual Modeling:
CLASSIFIER_OPTIONS = ["KNeighborsClassifier", "SVC", "GaussianNB", "RandomForestClassifier", "KMeans", "HistGradientBoostingClassifier"]
CM_IMAGE = 'resources/icons/cm_paradigm.png'
# CARS --> Pre-filtering:
PREFILTERING_IMAGE = 'resources/icons/pre_paradigm.png'
# CARS --> Post-filtering:
POSTFILTERING_IMAGE = 'resources/icons/post_paradigm.png'
POSTFILTERING_TYPE_OPTIONS = ['LARS', 'SIDE-LARS']
# Cross validation:
CROSS_VALIDATION_STRATEGIES = ["KFold", "RepeatedKFold", "ShuffleSplit", "LeaveOneOut"] # , "PredefinedKFold", "train_test_split"
# Metrics:
BINARY_RATING_METRICS = ["Precision", "Recall", "F1_Score", "AUC_ROC"]
DEFAULT_BINARY_RATING_METRICS = ["Precision", "Recall", "F1_Score"]
PREFERENCIAL_RATING_METRICS = ["MAE", "Precision", "Recall", "F1_Score", "RMSE", "MSE", "FCP", "MAP", "NDCG"]
DEFAULT_PREFERENCIAL_RATING_METRICS = ["MAE", "Precision", "Recall", "F1_Score"]
SCIKIT_LEARN_METRICS = ['Precision', 'Recall', 'F1 score', 'ROC-AUC', 'MAE', 'MSE', 'RMSE']
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
