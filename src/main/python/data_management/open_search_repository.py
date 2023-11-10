import logging

from data_management import config
from data_management.abstract_repository import AbstractRepository
from data_management.connection import Connection


class OpenSearchRepository(AbstractRepository):

    def __init__(self, host, http_auth, http_compress, use_ssl, verify_certs):
        self.conn = Connection(host, http_auth, http_compress, use_ssl, verify_certs)

    def get_df_data(self):
        '''
        Get all data of "analytics" from Open Search.
        :return: A dataframe with all data of "analytics".
        '''
        logging.info(f"Loading all data of {config.index_tasks} from Open Search.")
        # return self.conn.read_dataframe(index=config.index_tasks, query=config.match_all)
        return self.conn.read_dataframe(index=config.index_tasks, query=config.match_all)

    def get_df_data_foodbot(self):
        '''
        Get data filtering by virtual_space="Foodbots".
        :return: Dataframe related to virtual_space="Foodbots".
        '''
        logging.info('Loading df_data_foodbot.')
        return self.conn.read_dataframe(index=config.index_tasks, query=config.foodbot_match)

    def get_df_data_spaceship(self):
        '''
        Get data filtering by virtual_space="Spaceship".
        :return: Dataframe related to virtual_space="Spaceship".
        '''
        logging.info('Loading df_data_spaceship')
        return self.conn.read_dataframe(index=config.index_tasks, query=config.spaceship_match)

    def get_df_data_hospital(self):
        '''
        Get data filtering by virtual_space="Spaceship".
        :return: Dataframe related to virtual_space="Spaceship".
        '''
        logging.info('Loading df_data_spaceship')
        return self.conn.read_dataframe(index=config.index_tasks, query=config.hospital_match)
    
    def get_target_users_spaceship(self, target_user_spaceship_match):
        '''
        Get target users in virtual_space="Spaceship".
        :return: A list of target users in virtual_space="Spaceship".
        '''
        target_user_spaceship_match_modified={
        "size":"10000",
        "query": {
            "bool": {
                "must":  {"match": {"virtual_space_id":"Spaceship"} } ,
                "filter":{"range": {"@timestamp":{"gte":  target_user_spaceship_match}}}
               }
            }
        }

        logging.info('Loading target users in virtual_space="Spaceship"')
        target_users_spaceship_df = self.conn.read_dataframe(index=config.index_tasks, query=target_user_spaceship_match_modified)
        return target_users_spaceship_df['user_id'].unique().tolist()
