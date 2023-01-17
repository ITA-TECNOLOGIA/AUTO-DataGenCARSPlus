import logging

from configparser import NoOptionError, NoSectionError
from datagencars.generator.file_access.data_access import DataAccess

class ItemProfileAccess(DataAccess):
    '''
    Access to the values of the properties stored in the file that contain the item profiles (item_profile.conf).
    @author Maria del Carmen Rodriguez-Hernandez 
    '''

    def __init__(self, file_path):
        super().__init__(file_path)

    def get_number_profiles(self):
        '''
        Gets the number of item profiles.
        :return: The number of item profiles.
        '''
        number_profiles = None
        try:
            number_profiles = self.file_parser.getint(section='global', option='number_profiles')
        except (NoOptionError, NoSectionError) as e:            
            logging.error(e)
        return number_profiles
    
    def get_ranking_order_profile(self):
        '''
        Gets the order (e.g., ascending or descending) of the item profiles.
	    :return: The ranking order of the item profiles.
        '''        
        ranking_order_profile = None
        try:
            ranking_order_profile = self.file_parser.get(section='order', option='ranking_order_profile')
        except (NoOptionError, NoSectionError) as e:            
            logging.error(e)
        return ranking_order_profile

    def get_name_profile_from_pos(self, position):
        '''
        Gets the name of the item profile specified.
        :param position: The position of the item profile.
	    :return: The name of the item profile specified.
        '''        
        name_profile = None
        try:
            name_profile = self.file_parser.get(section='name', option=f'name_profile_{str(position)}')
        except (NoOptionError, NoSectionError) as e:            
            logging.error(e)
        return name_profile

    def get_name_profile_list(self):
        # sourcery skip: for-append-to-extend, use-fstring-for-concatenation
        '''
        Gets a list with the name of the item profiles.
        :return: A list with the name of the item profiles.
        '''
        name_profile_list = []
        number_profiles = self.get_number_profiles()
        try: 
            for pos in range(1, number_profiles+1):
                name_profile_list.append(self.file_parser.get(section='name', option='name_profile_'+str(pos)))
        except (NoOptionError, NoSectionError) as e:            
            logging.error(e)
        return name_profile_list

    def get_overlap_midpoint_left_profile(self):
        '''
        Gets a number that indicate if the mid point will overlap by the left.
	    :return: A number that indicate if the mid point will overlap by the left.
        '''        
        overlap_midpoint_left_profile = None
        try:
            overlap_midpoint_left_profile = self.file_parser.getint(section='overlap', option='overlap_midpoint_left_profile')
        except (NoOptionError, NoSectionError) as e:            
            logging.error(e)
        return overlap_midpoint_left_profile

    def get_overlap_midpoint_right_profile(self):
        '''
        Gets a number that indicate if the mid point will overlap by the right.
	    :return: A number that indicate if the mid point will overlap by the right.
        '''
        overlap_midpoint_right_profile = None
        try:
            overlap_midpoint_right_profile = self.file_parser.getint(section='overlap', option='overlap_midpoint_right_profile')
        except (NoOptionError, NoSectionError) as e:            
            logging.error(e)
        return overlap_midpoint_right_profile
    
