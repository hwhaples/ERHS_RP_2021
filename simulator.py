# Implements a simulation object that recieves weather data, photovoltaic measurement, and a defined system topology.
# These inputs are used to generate and return an expectation.
import numpy as np

class Simulator():

    def __init__(self, weather, pv_measurement, system_model, realtime=False):
        '''
        Constructor for a Simulator object, requiring data stream inputs.
        Parameters:
            weather           -- (obj) weather object providing streamed weather data
            pv_measurement    -- (obj) pv_measurement object providing streamed performance measurements of a real PV system
            system_model      -- (obj) system_model object providing streamed performance estimates of a simulated PV system topology
            real_time         -- (bool) flag, if TRUE simulator is running in realtime operation
        '''
        self.weather = weather
        self.pv_measurement = pv_measurement
        self.system_model = system_model
    
    def _calc_expectation(self):
        '''
        Signals system_model object to calculate expected performance values
        '''
        expectation = system_model._calc_expectation(self.weather)
        return expectation

    def _update_data(self):
        '''
        Signals weather and pv_measurement objects to update 
        '''
        weather.update()
        pv_measurement.update()
        return

    def _calc_difference(self):
        '''
        Calculate the difference at the current timestep between the pv_measurement and the system_model
        '''
        system_expectation = self._calc_expectation()
        pv_expectation = self.pv_measurement

    def _calc_tracking_error(self,lookback=np.Inf):

    def _save_data(self,filepath,filename):
        '''
        Saves simulator data to the filepath under the filename.
        '''