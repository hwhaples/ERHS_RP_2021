# Uses the PVLIB library to define photovoltaic objects that we can choose to use in our simulations.
# Our software for now will focus on fixed-tilt photovoltaic installations.

import component
import pvlib as pv
import math
import pytz

from datetime import datetime, timedelta


class photovoltaics(component):
    '''
    Defines a photovoltaic system component for a system model
    '''

    def __init__(self,name,location):
        self.name = name
        self.location = location

        self.latitude = location.latitude
        self.longitude = location.longitude


    def __days_since_soy(self,time):
        '''
        Calculate the days since the start of the year (soy) from a date time.

        Args:
            time: (datetime) datetime object to return days from stat of year
        
        Returns: 
            days_since_soy: number of days since the start of the year
        '''
        year = time.year
        soy = datetime(year,1,1)
        days_since_soy = time - soy
        return days_since_soy.days


    def __get_lstm(self,time,tz=None):
        '''
        Calculates the local standard time meridian (LSTM)

        Args:
            time: (datetime) datetime object to return LSTM
            tz: (pytz) python timezone object, default set to none - results in EDT (UTC-4)
        
        Returns:
            lstm: local standard time meridian
        '''
        default_tz = pytz.timezone('UTC')
        if time.tzinfo is None:
            time = default_tz.localize(time)
        else:
            time = tz.localize(time)
        
        utc_time = time.astimezone('UTC')
        delta_t_utc = time-utc_time                     # Difference in hours local from GMT
        lstm = 15 * delta_t_utc                         # Local Standard Time Meridian
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
        Calculates the time correction factor (TC) in minutes

        Args:
            time: (datetime) datetime object to return time correction
        
        Returns:
            tc: time correction factor
        '''
        lstm = self.__get_lstm(time)
        eot = self.__get_eot(time)
        tc = 4 * (self.longitude - lstm) + eot
        return tc
    
    def __get_lst(self,time):
        '''
        Caluculates the local solar time (lst) from the local time and time correction

        Args:
            time: (datetime) datetime object to return local solar time
        
        Returns:
            lst: (datetime) local solar time
        '''
        lt = time                             # the local datetime
        tc = self.__get_tc(self,time)
        lst = lt + timedelta(hours=(tc/60))   # local solar time
        return lst
    
    def __get_hra(self, time):
        '''
        Calculates the hour angle (HRA). By definition the HRA is 0 at solar noon.
        The earth rotates at 15 deg per hour. Each hour away from solar noon corresponds
        to angular motion of the sun by 15 deg. Morning sun has a negative angle

        Args:
            time: (datetime) datetime object to return hour angle
        
        Returns:
            hra: hour angle in degrees
        '''
        lst = self.__get_lst(time)
        return 15 * (lst - 12)
    
    def get_declination(self,time):
        '''
        Calculates the solar declination in degrees at a given time.

        Args:
            time: (dateimte) datetime object to return declination
        
        Returns:
            declination: estimated solar declination at specified time
        '''
        d = self.__days_since_soy(time)
        earth_angle = math.radians((360/365) * (d - 81))
        return 23.45 * math.sin(earth_angle)

    def get_sun_position(self,time,location):
        '''
        Calculates the solar elevation and azimuth.

        Args:
            time: (datetime) datetime object to return solar position
            location: (location) location object containing latitude and longitude
        
        Returns:
            elevation: solar elevation
            azimuth: solar azimuth
        '''
        # All must be converted to radians for colculations
        declination = math.radians(self.get_declination(time))
        latitude = math.radians(location.latitude)
        hra = math.radians(self.__get_hra(time))

        elevation_rad = math.asin(
            math.sin(declination)*math.sin(latitude) +
            math.cos(declination)*math.cos(latitude)*math.cos(hra)
        )

        azimuth_rad = math.acos(
            (math.sin(declination)*math.cos(latitude) - 
            math.cos(declination)*math.sin(latitude)*math.cos(hra)) / 
            math.cos(elevation_rad)
        )

        elevation = math.degrees(elevation_rad)
        azimuth = math.degrees(azimuth_rad)

        return elevation, azimuth