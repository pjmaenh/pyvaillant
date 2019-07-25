import logging
import time
from . import _BASE_URL, NoDevice, NoValidMode, NoValidSystemMode, postRequest

LOG = logging.getLogger(__name__)

_GETTHERMOSTATDATA_REQ = _BASE_URL + "api/getthermostatsdata"
_SETTEMP_REQ = _BASE_URL + "api/setminormode"
_SETSYSTEMMODE_REQ = _BASE_URL + "api/setsystemmode"


class VaillantThermostatData:
    """
    Representation of a Vaillant/Bulex Thermostat
    """

    def __init__(self, authData):
        self.name = None                    # Module Name        
        self.temp = None                    # Current Temperature
        self.setpoint_temp = None           # Setpoint Temperature
        #self.setpoint_mode = None          # Setpoint Mode (manual, away, hwb, program)
        self.setpoint_manual = False        # Manual setpoint
        self.setpoint_away = False          # Away
        self.setpoint_hwb = False           # Hot Water Boost
        self.system_mode = None             # System Mode (winter, summer, frostguard)
        self.token = authData.accessToken   # Access Token
        self.update()                       # Get latest data        
    
    def update(self):
        # Get latest data from server
        postParams = {
            "access_token": self.token,
            "device_type": "NAVaillant",
        }
        resp = postRequest(_GETTHERMOSTATDATA_REQ, postParams)
        if resp is None:
            raise NoDevice("No thermostat data returned by Netatmo server")
        self.rawData = resp['body']

        self.devList = self.rawData['devices']
        if not self.devList:
            raise NoDevice("No thermostat available")
        
        if not self.rawData['devices'][0]['modules']:
            raise NoDevice("No modules available")

        self.modList = self.devList[0]['modules']

        # Get name, current temperature and setpoint temperature
        if 'module_name' in self.rawData['devices'][0]['modules'][0]:
            self.name = self.rawData['devices'][0]['modules'][0]['module_name']
        if 'temperature' in self.rawData['devices'][0]['modules'][0]['measured']:
            self.temp = self.modList[0]['measured']['temperature']
        if 'setpoint_temp' in self.modList[0]['measured']:
            self.setpoint_temp = self.modList[0]['measured']['setpoint_temp']
        
        # Get active setpoint mode(s)
        self.setpoint_manual = self.modList[0]['setpoint_manual']['setpoint_activate']
        self.setpoint_away = self.modList[0]['setpoint_away']['setpoint_activate']
        self.setpoint_hwb = self.devList[0]['setpoint_hwb']['setpoint_activate']

        # Get setpoint mode
        '''
        if self.modList[0]['setpoint_manual']['setpoint_activate']:
            self.setpoint_mode = "manual"
        elif self.modList[0]['setpoint_away']['setpoint_activate']:
            self.setpoint_mode = "away"
        elif self.devList[0]['setpoint_hwb']['setpoint_activate']:
            self.setpoint_mode = "hwb"
        else:
            self.setpoint_mode = "program"
        '''

        # Get system mode
        self.system_mode = self.devList[0]['system_mode']

        #self.devices = {d['_id']: d for d in self.rawData['devices']}
        '''
        # Do we need this?
        self.modules = dict()
        self.therm_program_list = dict()
        self.zones = dict()
        self.timetable = dict()
        for i in range(len(self.rawData['devices'])):
            nameDevice = self.rawData['devices'][i]['station_name']
            if nameDevice not in self.modules:
                self.modules[nameDevice] = dict()
            for m in self.rawData['devices'][i]['modules']:
                self.modules[nameDevice][m['_id']] = m
            for p in self.rawData['devices'][i]['modules'][0]['therm_program_list']:
                self.therm_program_list[p['program_id']] = p
            for z in self.rawData['devices'][i]['modules'][0]['therm_program_list'][0]['zones']:
                self.zones[z['id']] = z
            for o in self.rawData['devices'][i]['modules'][0]['therm_program_list'][0]['timetable']:
                self.timetable[o['m_offset']] = o
        self.default_device = list(self.devices.values())[0]['station_name']

        self.default_module = list(self.modules[self.default_device].values())[0]['module_name']
        '''

    # Do we need this?
    '''
    def lastData(self, device=None, exclude=0):
        s = self.deviceByName(device)
        if not s:
            return None
        lastD = dict()
        zones = dict()
        # Define oldest acceptable sensor measure event
        limit = (time.time() - exclude) if exclude else 0
        dm = s['modules'][0]['measured']
        self.setpoint_manual = self.modList[0]['setpoint_manual']['setpoint_activate']
        self.setpoint_away = self.modList[0]['setpoint_away']['setpoint_activate']
        if self.setpoint_manual:
            ds = "manual"
        elif self.setpoint_away:
            ds = "away"
        else:
            ds = "program"
        dz = s['modules'][0]['therm_program_list'][0]['zones']
        for module in s['modules']:
            dm = module['measured']
            setpoint_manual = self.modList[0]['setpoint_manual']['setpoint_activate']
            setpoint_away = self.modList[0]['setpoint_away']['setpoint_activate']
            if self.setpoint_manual:
                ds = "away"
            elif self.setpoint_away:
                ds = "manual"
            else:
                ds = "auto"
            dz = module['therm_program_list'][0]['zones']
            if dm['time'] > limit:
                lastD[module['module_name']] = dm.copy()                # lastD['setpoint_mode'] = ds
                lastD[module['module_name']]['setpoint_mode'] = ds
                # For potential use, add battery and radio coverage information to module data if present
                for i in ('battery_vp', 'rf_status', 'battery_percent'):
                    if i in module:
                        lastD[module['module_name']][i] = module[i]
                zones[module['module_name']] = dz.copy()
        return lastD
    '''

    # Do we need this?
    '''
    def deviceById(self, did):
        return None if did not in self.devices else self.devices[did]
    '''

    # Do we need this?
    '''    
    def deviceByName(self, device):
        if not device:
            device = self.default_device
        for key, value in self.devices.items():
            if value['station_name'] == device:
                return self.devices[key]

    '''

    # Do we need this?
    '''
    def moduleById(self, mid):
        for device, mod in self.modules.items():
            if mid in self.modules[device]:
                return self.modules[device][mid]
        return None
    '''

    # Do we need this?
    '''
    def moduleByName(self, module=None, device=None):
        if not module and not device:
            return self.default_module
        elif device and module:
            if device not in self.modules:
                return None
            for mod_id in self.modules[device]:
                if self.modules[device][mod_id]['module_name'] == module:
                    return self.modules[device][mod_id]
        elif not device and module:
            for device, mod_ids in self.modules.items():
                for mod_id in mod_ids:
                    if self.modules[device][mod_id]['module_name'] == module:
                        return self.modules[device][mod_id]
        else:
            return list(self.modules[device].values())[0]
        return None
    '''

    def setThermPoint(self, setpointMode, setpointTemperature, endTimeOffset, deviceId = None, moduleId = None):
        """
        Set the preferred temperature and/or change mode
        """
        if setpointMode not in ["program", "manual", "away", "hwb"]:
            raise NoValidMode("No valid setpoint mode: [{}]".format(setpointMode))

        if setpointMode == "program":
            #Deactivate old mode(s)
            if(self.setpoint_away):
                self.deActivate("away")
            if(self.setpoint_hwb):
                self.deActivate("hwb")                
            if(self.setpoint_manual):
                self.deActivate("manual")                
            return

        postParams = {"access_token": self.token}
        postParams['device_id'] = deviceId if deviceId else self.devList[0]['_id']
        postParams['module_id'] = moduleId if moduleId else self.modList[0]['_id']            
        postParams['setpoint_mode'] = setpointMode            
        postParams['activate'] = "true"
        if setpointMode == "manual":
            postParams['setpoint_endtime'] = int(time.time() + endTimeOffset)
            postParams['setpoint_temp'] = setpointTemperature
        if setpointMode == "hwb":
            postParams['setpoint_endtime'] = int(time.time() + endTimeOffset)
        return postRequest(_SETTEMP_REQ, postParams)

    def deActivate(self, setpointMode, deviceId = None, moduleId = None):
        '''
        Deactivate a setpoint mode
        '''
        if setpointMode not in ["manual", "away", "hwb"]:
            raise NoValidMode("No valid setpoint mode: [{}]".format(setpointMode))        
        postParams = {"access_token": self.token}
        postParams['device_id'] = deviceId if deviceId else self.devList[0]['_id']
        postParams['module_id'] = moduleId if moduleId else self.modList[0]['_id']
        postParams['activate'] = "false"
        postParams['setpoint_mode'] = setpointMode
        return postRequest(_SETTEMP_REQ, postParams)

    def setSystemMode(self, systemMode, deviceId = None, moduleId = None):
        """
        Set the system mode (winter, summer, frostguard)
        """
        if systemMode not in ["winter", "summer", "frostguard"]:
            raise NoValidSystemMode("No valid system mode: [{}]".format(systemMode))
        postParams = {"access_token": self.token}

        postParams['device_id'] = deviceId if deviceId else self.devList[0]['_id']
        postParams['module_id'] = moduleId if moduleId else self.modList[0]['_id']
        postParams['system_mode'] = systemMode

        return postRequest(_SETSYSTEMMODE_REQ, postParams)

    def printStatus(self):
        print("Thermostat:      \t {}".format(self.name))
        print("Current temp:    \t {}".format(self.temp))
        print("Target temp:     \t {}".format(self.setpoint_temp))
        print("System mode:     \t {}".format(self.system_mode))
        print("Manual setpoint? \t {}".format(self.setpoint_manual))            
        print("Away?            \t {}".format(self.setpoint_away))
        print("Hot Water Boost? \t {}".format(self.setpoint_hwb))
        #print(thermostat.data.setpoint_mode)
        print("")

