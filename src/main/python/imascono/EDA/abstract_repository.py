from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    def get_df_data(self):
        pass

    @abstractmethod
    def get_df_data_foodbot(self):
        pass

    @abstractmethod
    def get_df_data_spaceship(self):
        pass

    @abstractmethod
    def get_target_users_spaceship(self, target_user_spaceship_match):
        pass
