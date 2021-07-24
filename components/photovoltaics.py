# Uses the PVLIB library to define photovoltaic objects that we can choose to use in our simulations.
# Our software for now will focus on fixed-tilt photovoltaic installations.

import component
import pvlib as pv
import math

class photovoltaics(component):
    '''
    Defines a photovoltaic system component for a system model
    '''

    def __init__(self,name,location):
        self.name = name
        self.location = location

        self.latitude = location.latitude
        self.longitude = location.longitude

    def __get_lstm(self,time):
        '''
        Calculates the local standard time meridian (LSTM)

        Args:
            time: (datetime) datetime object to return LSTM
        
        Returns:
            lstm: local standard time meridian
        '''
        delta_t_gmt = 1                                 # Difference in hours local from GMT
        lstm = 15 * delta_t_gmt                         # Local Standard Time Meridian
        return lstm

    def __get_eot(self,time):
        '''
        Calculates the equation of time

        Args:
            time: (datetime) datetime object to return eot
        
        Returns:
            eot: equation of time correction
        '''
        # TODO: calculate days required
        d = 1                                           # Days since start of the year
        B = 360 / 365 * (d - 81)
        B = math.radians(B)                             # Convert degrees to radians
        
        EoT = 9.87 * math.sin(2 * B) - 7.53 * math.cos(2 * B) - 1.5 * (B)
        return EoT
    
    def __get_tc(self,time):
        '''
        Calculates the time correction factor (TC)

        Args:
            time: (datetime) datetime object to return time correction
        
        Returns:
            tc: time correction factor
        '''
        lstm = self.__get_lstm(time)
        eot = self.__get_eot(time)
        tc = 4 * (self.longitude - lstm) + eot
        return tc

    def get_solar_time(self, time):
        '''
        Converts datetime into solar time.
        
        Args:
            time: (datetime) datetime object to be converted to solar time.
        
        Returns:
            solar_time: solar time object
        '''
        lstm = self.__get_lstm(time)
        eot = self.__get_eot(time)


    def get_sun_position(self):
        '''
        Calculates the solar azimuth and elevation given time
        '''

