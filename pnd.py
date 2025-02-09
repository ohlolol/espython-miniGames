import pndSRC as mypnd
import pndConfig as cfg
import ntptime
import ujson
import time
import machine
import array
import gc
import menu



class rt():
    
    storage = mypnd.storage()
    wifi = mypnd.wifi()
    Psystem = mypnd.system()
    lastTry = 0
    cycle = 0
    looping = 0
    cfg = cfg
    
    def run(self):
        self.cycle = 1
        while True:
            try:
               ## main loop
                gc.collect()
                machine.idle()
                print(self.Psystem.status())
                
                x = menu.TouchScreen(self)
                self.Running = True
                while (self.Running == True):
                    time.sleep(1)
            except OSError as e:
                mypnd.ecx.handle(self,e)

    def backgroundTask(self):

        lhttp = mypnd.webserver()
        print('starting Webserver...')
        
        ## method with main loop goes here
        lhttp.showStatusPage()

    def init(self, lastTry):
        try:
            self.Psystem.setCallback(self)
            i = 0
            self.lastTry = lastTry
            self.wifi.connect()
            ntptime.host = cfg.defaults.gc_ntp_host
            self.cycle = 1
            try:
                ntptime.settime()
            except:
                pass
            if hasattr(cfg.tasks, "gc_sensors"):
                self.Sensors = {}
                for sens in cfg.tasks.gc_sensors:
                    if cfg.tasks.gc_sensors[sens]['ADC']:
                        self.Sensors[i] = mypnd.adcsens(cfg.tasks.gc_sensors[sens]['name'],cfg.tasks.gc_sensors[sens]['pin'])
                    else:
                        self.Sensors[i] = mypnd.sens(cfg.tasks.gc_sensors[sens]['name'],cfg.tasks.gc_sensors[sens]['type'],cfg.tasks.gc_sensors[sens]['pin'])
                    i += 1
            #if hasattr(cfg.tasks, "gc_display"):
                #self.dispService = dispService(); ## needs new implementation for CYD
            if hasattr(cfg.defaults, "gc_battery"):
                self.looping = (cfg.defaults.gc_looping * 1000) * 60
                self.data = self.storage.read()
                if(machine.reset_cause() == 4):
                    self.cycle = self.data["cycle"]
                    
        except OSError as e:
            mypnd.ecx.handle(mypnd.ecx(),self,e)
        
        
class pndCBObejct():
    me = object()
    caller = object()
    
    def __init__(self, caller):
        self.me = self
        self.caller = caller
        
    def getMe(self):
        return self.me
    
    def getCaller(self):
        return self.caller
    
