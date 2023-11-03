import ast
import time, random, math
from datetime import datetime
import numpy as np
import pandas as pd
import warnings

from datagencars.synthetic_dataset.generator.generator_instance.generator_instance import GeneratorInstance
from datagencars.synthetic_dataset.generator.generator_output_file.generator_file import GeneratorFile
from datagencars.synthetic_dataset.generator.access_schema.access_schema import AccessSchema


class GeneratorBehaviorFile(GeneratorFile):
    '''     
    Generates user behaviors.
    @author Marcos Caballero Yus
    '''

    def __init__(self, generation_config, behavior_schema, item_df, item_schema):
        warnings.filterwarnings("ignore", category=FutureWarning)
        # Schema access: generation_config.conf
        super().__init__(generation_config, behavior_schema)
        self.min_interval = self.access_generation_config.get_minimum_interval_behavior()
        self.max_interval = self.access_generation_config.get_maximum_interval_behavior()
        self.num_users = self.access_generation_config.get_number_user()
        self.num_contexts = self.access_generation_config.get_number_context()
        self.num_behaviors = self.access_generation_config.get_number_behavior()
        self.session_time = self.access_generation_config.get_session_time()
        self.door = self.access_generation_config.get_initial_position()
        self.minimum_radius = self.access_generation_config.get_minimum_radius()
        self.maximum_radius = self.access_generation_config.get_maximum_radius()
        self.interaction_threshold = self.access_generation_config.get_interaction_threshold() # The maximum distance for an object to be considered interactable.
        self.minimum_year_ts = time.mktime(datetime.strptime(self.access_generation_config.get_minimum_date_timestamp(), "%Y").timetuple()) #%Y-%m-%d
        self.maximum_year_ts = time.mktime(datetime.strptime(self.access_generation_config.get_maximum_date_timestamp(), "%Y").timetuple()) #%Y-%m-%d

        # Item schema: item_schema.conf
        item_schema_access = AccessSchema(file_str=item_schema)
        self.rooms = item_schema_access.get_subattribute_input_parameters_dict_from_name_attribute('object_position')
        
        self.item_df = item_df
        if 'object_position' in self.item_df.columns and 'object_action_types' in self.item_df.columns:
            try:
                self.item_df['object_position'] = self.item_df['object_position'].apply(lambda x: str(x))
                self.item_df['object_action_types'] = self.item_df['object_action_types'].apply(lambda x: str(x))
            except:
                pass

        self.file_df = pd.DataFrame({'user_id': [], 'object_action': [], 'user_position': [], 'behavior_id': [], 'item_id': [], 'context_id': [], 'timestamp': []})
        self.behavior_id = 1
        self.z = 5 # Fixed value of z for this scenario

    def generate_random_position_within_cylinder (self, last_position):
        """
        Generate a random position within a circle around the given last_position.
        :param last_position: The center of the circle, a list containing the x and y coordinates.
        :return: A tuple with the x and y coordinates of the new random position within the circle and room boundaries.
        """
        angle = 2 * math.pi * random.random()
        radius = random.uniform(self.minimum_radius, self.maximum_radius)
        r = radius * math.sqrt(random.random())
        new_x = last_position[0] + r * math.cos(angle)
        new_y = last_position[1] + r * math.sin(angle)

        # Check if the new position is within the room boundaries
        for room in self.rooms:
            if (room['x_min'] <= new_x <= room['x_max']) and (room['y_min'] <= new_y <= room['y_max']):
                return new_x, new_y, self.z

        # If the new position is outside the room boundaries, try again
        return self.generate_random_position_within_cylinder (last_position)
    
    def check_interaction_with_nearby_objects(self, user_position, item_df):
        '''
        Check if the user_position is within the interaction_threshold of any objects in the item_df.
        :param user_position: A list containing the x and y coordinates of the user position.
        :param item_df: A DataFrame containing information about objects and their positions.
        :param interaction_threshold: The maximum distance for an object to be considered interactable.
        :return: A tuple with the item_id of the interacted object and the chosen object_action, or (None, None) if no interaction.
        '''
        for _, row in item_df.iterrows():
            object_position = eval(row['object_position']) # Extract x, y and z coordinates #[:2]
            distance = math.sqrt((user_position[0] - object_position[0]) ** 2 + (user_position[1] - object_position[1]) ** 2 + (user_position[2] - object_position[2]) ** 2)
            if distance < self.interaction_threshold:
                if random.random() < 0.5:  # 50% chance to interact
                    # Choose a random action from the allowed actions
                    """
                    Cuando se utiliza la función eval(), Python intenta evaluar la cadena como si fuera código Python. En tu caso, parece que row['object_action_types'] es una cadena que representa una lista de nombres de acciones, como "Open", "Close", etc. Cuando eval() intenta evaluar esta cadena, busca variables con estos nombres en el contexto actual. Como no existen tales variables, se produce un error.
                    """
                    # allowed_actions = [action for action in eval(row['object_action_types']) if action not in ['Close', 'Pause']]
                    # allowed_actions = [action for action in ast.literal_eval(row['object_action_types']) if action not in ['Close', 'Pause']]
                    allowed_actions = [action.strip() for action in row['object_action_types'].split(',') if action.strip() not in ['Close', 'Pause']]
                    object_action = random.choice(allowed_actions) if allowed_actions else None
                    return row['item_id'], object_action
        return None, None
    
    def add_behavior_record(self, user_id, object_action, item_id, context_id, behavior_id, user_position, timestamp):
        '''
        Create and add a new behavior record to the file_df DataFrame.
        :param user_id: The id of the user.
        :param object_action: The action performed on the object.
        :param item_id: The id of the item.
        :param context_id: The id of the context.
        :param behavior_id: The id of the behavior.
        :param user_position: A list containing the x and y coordinates of the user position, or np.nan if not applicable.
        :param timestamp: The timestamp of the action.
        '''
        new_record = {
            'behavior_id': behavior_id,
            'user_id': user_id,
            'object_action': object_action,
            'item_id': item_id,
            'context_id': context_id,
            'user_position': user_position,
            'timestamp': timestamp
        }

        # Convert _id columns to integers except for rows with item_id == 'Position'
        if item_id != 'Position':
            new_record['item_id'] = int(item_id)
            new_record['behavior_id'] = int(behavior_id)

        self.file_df = self.file_df.append(new_record, ignore_index=True)
        self.behavior_id += 1

    def generate_session_times(self, user_id, context_id, item_df, current_time, reset_position=True):
        '''
        Generate user behavior records within a session.
        :param user_id: The id of the user.
        :param context_id: The id of the context.
        :param item_df: A DataFrame containing information about objects and their positions.
        :param current_time: The start time of the session.
        '''
        session_end = current_time + random.uniform(0, self.session_time)  # Add a random interval to session_start
        while current_time < session_end and self.behavior_id <= self.num_behaviors:
            # Verify if there are records for the user
            user_records = self.file_df.loc[self.file_df['user_id'] == user_id]
            # If there are records, get the last position
            if user_records.empty or reset_position:
                # print("initial position user", user_id)
                last_position = self.door #[:2] # Get x, y and z coordinates
                self.add_behavior_record(
                        behavior_id=self.behavior_id,
                        user_id=user_id,
                        object_action='Update',
                        item_id='Position',
                        context_id=context_id,
                        user_position=last_position, 
                        timestamp=current_time
                )
                reset_position = False
            else:
                # Obtain the last position of the user if the action was an update of the position
                user_position_records = user_records.loc[(user_records['object_action'] == 'Update') & (user_records['item_id'] == 'Position')]
                if not user_position_records.empty:
                    last_position = user_position_records['user_position'].values[-1]

            action = random.choice(['move', 'interact', 'end_session'])
            if action == 'move':
                # print("move")
                new_position = self.generate_random_position_within_cylinder (last_position)
                self.add_behavior_record(
                        user_id=user_id,
                        object_action='Update',
                        item_id='Position',
                        context_id=context_id,
                        behavior_id=self.behavior_id,
                        user_position=[*new_position],
                        timestamp=current_time
                )
            elif action == 'interact':
                object_id, object_action = self.check_interaction_with_nearby_objects(last_position, item_df)
                if object_id is not None:
                    # print("interact object")
                    self.add_behavior_record(
                        user_id=user_id,
                        object_action=object_action,
                        item_id=object_id,
                        context_id=np.nan,
                        behavior_id=self.behavior_id,
                        user_position=np.nan,
                        timestamp=current_time
                    )

                    last_object_action = None
                    if not self.file_df.empty:
                        last_object_action = self.file_df['object_action'].iloc[-1]
                        last_user_id = self.file_df['user_id'].iloc[-1]
                        last_object_id = self.file_df['item_id'].iloc[-1]
                        last_current_time = self.file_df['timestamp'].iloc[-1]
                    if last_object_action == 'Open':
                        self.add_behavior_record(
                            user_id=last_user_id,
                            object_action='Close',
                            item_id=last_object_id,
                            context_id=np.nan,
                            behavior_id=self.behavior_id,
                            user_position=np.nan,
                            timestamp=last_current_time + random.uniform(self.min_interval, self.max_interval)
                        )
                    elif last_object_action == 'Play':
                        self.add_behavior_record(
                            user_id=last_user_id,
                            object_action='Pause',
                            item_id=last_object_id,
                            context_id=np.nan,
                            behavior_id=self.behavior_id,
                            user_position=np.nan,
                            timestamp=last_current_time + random.uniform(self.min_interval, self.max_interval)
                        )
                else:
                    # print("interact move")
                    new_position = self.generate_random_position_within_cylinder(last_position)
                    self.add_behavior_record(
                        user_id=user_id,
                        object_action='Update',
                        item_id='Position',
                        context_id=context_id,
                        behavior_id=self.behavior_id,
                        user_position=[*new_position],
                        timestamp=current_time
                    )

            elif action == 'end_session':
                # print("end_session user", user_id)
                break

            # Update the current time based on a random interval between 1 second and 5 minutes
            current_time += random.uniform(self.min_interval, self.max_interval)

    def generate_file(self):
        '''
        Generates the behavior file.   
        :return: A dataframe with behavior information (user_id, object_action, user_position, behavior_id, item_id, context_id, timestamp)
        '''
        print(f'Total of behaviors to generate: {self.num_behaviors}')
        # print('Generating instances by behavior.')

        instance_generator = GeneratorInstance(schema_access=self.schema_access)
        for _ in range(self.num_behaviors):
            attribute_list = instance_generator.generate_instance()
            # self.file_df.loc[len(self.file_df.index)] = attribute_list
        
        while self.behavior_id <= self.num_behaviors:
            user_id = random.randint(1, self.num_users)  # Pick a random user_id
            context_id = random.randint(1, self.num_contexts)  # Pick a random context_id
            session_start = random.uniform(self.minimum_year_ts, self.maximum_year_ts)            
            self.generate_session_times(user_id, context_id, self.item_df, session_start, reset_position=True) # Reset the user's position at the beginning of each session

        # Convert timestamps to the specified format
        self.file_df['timestamp'] = pd.to_datetime(self.file_df['timestamp'], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')

        # Sort by user_id
        self.file_df = self.file_df.sort_values('user_id')
        
        return self.file_df.copy()
